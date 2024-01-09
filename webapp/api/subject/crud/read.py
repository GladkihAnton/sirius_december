from typing import List, Optional

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from webapp.api.subject.router import subject_router
from webapp.crud.subject import get_all, get_subject_by_id
from webapp.db.postgres import get_session
from webapp.models.sirius.group_subject import GroupSubject
from webapp.models.sirius.subject import Subject
from webapp.models.sirius.teacher import Teacher
from webapp.schema.subject import SubjectRead
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@subject_router.get('/', response_model=List[SubjectRead])
async def read_all(
    group_id: Optional[int] = None,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if group_id is None:
        results = await get_all(session)

    else:
        query = (
            select(Subject)
            .options(joinedload(Subject.teacher).joinedload(Teacher.user))
            .join(GroupSubject, Subject.id == GroupSubject.subject_id)
            .where(GroupSubject.group_id == group_id)
        )
        results = (await session.execute(query)).unique().scalars().all()

    json_result = [SubjectRead.model_validate(result).model_dump(mode='json') for result in results]

    return ORJSONResponse(json_result)


@subject_router.get('/{subject_id}', response_model=SubjectRead)
async def read_one(
    subject_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    result = await get_subject_by_id(session, subject_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    json_result = SubjectRead.model_validate(result).model_dump(mode='json')

    return ORJSONResponse(json_result)
