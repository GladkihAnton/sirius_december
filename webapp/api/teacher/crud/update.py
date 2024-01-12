from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.teacher.router import teacher_router
from webapp.cache.cache import redis_remove
from webapp.crud.teacher import teacher_crud
from webapp.db.postgres import get_session
from webapp.models.sirius.teacher import Teacher
from webapp.schema.teacher import TeacherInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@teacher_router.put('/update/{teacher_id}')
async def update(
    teacher_id: int,
    body: TeacherInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        result = await teacher_crud.update(session, body, teacher_id)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    if not result:
        raise HTTPException(detail='Teacher not found', status_code=status.HTTP_404_NOT_FOUND)

    await redis_remove(Teacher.__name__, teacher_id)

    return ORJSONResponse(content={'detail': 'Teacher updated successfully'}, status_code=status.HTTP_200_OK)
