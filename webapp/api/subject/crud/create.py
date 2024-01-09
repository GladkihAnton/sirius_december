from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.subject.router import subject_router
from webapp.crud.institution import get_institution_by_id
from webapp.crud.subject import subject_crud
from webapp.crud.teacher import get_teacher_by_id
from webapp.db.postgres import get_session
from webapp.schema.subject import SubjectInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@subject_router.post('/create')
async def create(
    body: SubjectInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    # # Check if teacher exists for creating a relationship
    # if await get_teacher_by_id(session, body.teacher_id) is None:
    #     raise HTTPException(detail='Teacher not found', status_code=status.HTTP_404_NOT_FOUND)

    # # Check if institution exists for creating a relationship
    # if await get_institution_by_id(session, body.institution_id) is None:
    #     raise HTTPException(detail='Institution not found', status_code=status.HTTP_404_NOT_FOUND)

    try:
        created_id = await subject_crud.create(session, body)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={'id': created_id}, status_code=status.HTTP_201_CREATED)
