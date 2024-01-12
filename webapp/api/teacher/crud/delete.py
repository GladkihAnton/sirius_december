from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.teacher.router import teacher_router
from webapp.cache.cache import redis_remove
from webapp.crud.teacher import teacher_crud
from webapp.db.postgres import get_session
from webapp.models.sirius.teacher import Teacher
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@teacher_router.delete('/delete/{teacher_id}')
async def delete(
    teacher_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if not await teacher_crud.delete(session, teacher_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await redis_remove(Teacher.__name__, teacher_id)

    return ORJSONResponse(content={'detail': 'Teacher deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
