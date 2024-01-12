from typing import List, Optional

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from webapp.api.student.router import student_router
from webapp.cache.cache import redis_get, redis_set
from webapp.crud.const import SKIP_LIMIT
from webapp.crud.student import get_all, get_student_by_id
from webapp.db.postgres import get_session
from webapp.models.sirius.student import Student
from webapp.schema.student import StudentRead
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@student_router.get('/page/{page}', response_model=List[StudentRead])
async def read_all(
    page: int,
    group_id: Optional[int] = None,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if group_id is None:
        results = await get_all(session, page)

    else:
        query = (
            select(Student)
            .where(Student.group_id == group_id)
            .options(selectinload(Student.user))
            .limit(SKIP_LIMIT)
            .offset(page)
        )
        results = (await session.scalars(query)).all()

    json_result = [StudentRead.model_validate(result).model_dump(mode='json') for result in results]

    return ORJSONResponse(json_result)


@student_router.get('/{student_id}', response_model=StudentRead)
async def read_one(
    student_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    cached = await redis_get(Student.__name__, student_id)
    if cached:
        return ORJSONResponse(cached)

    result = await get_student_by_id(session, student_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    json_result = StudentRead.model_validate(result).model_dump(mode='json')
    await redis_set(Student.__name__, student_id, json_result)

    return ORJSONResponse(json_result)
