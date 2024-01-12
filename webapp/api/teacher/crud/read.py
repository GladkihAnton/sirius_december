from typing import List, Optional

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from webapp.api.teacher.router import teacher_router
from webapp.cache.cache import redis_get, redis_set
from webapp.crud.const import SKIP_LIMIT
from webapp.crud.teacher import get_all, get_teacher_by_id
from webapp.db.postgres import get_session
from webapp.models.sirius.teacher import Teacher
from webapp.schema.teacher import TeacherRead
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@teacher_router.get('/page/{page}', response_model=List[TeacherRead])
async def read_all(
    page: int,
    institution_id: Optional[int] = None,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if institution_id is None:
        results = await get_all(session, page)

    else:
        query = (
            select(Teacher)
            .where(Teacher.institution_id == institution_id)
            .options(selectinload(Teacher.user))
            .limit(SKIP_LIMIT)
            .offset(page)
        )
        results = (await session.scalars(query)).all()

    json_results = [TeacherRead.model_validate(result).model_dump(mode='json') for result in results]

    return ORJSONResponse(json_results)


@teacher_router.get('/{teacher_id}', response_model=TeacherRead)
async def read_one(
    teacher_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    cached = await redis_get(Teacher.__name__, teacher_id)
    if cached:
        return ORJSONResponse(cached)

    result = await get_teacher_by_id(session, teacher_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    json_result = TeacherRead.model_validate(result).model_dump(mode='json')
    await redis_set(Teacher.__name__, teacher_id, json_result)

    return ORJSONResponse(json_result)
