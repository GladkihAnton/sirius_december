from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.subject.router import subject_router
from webapp.cache.cache import redis_remove
from webapp.crud.subject import subject_crud
from webapp.db.postgres import get_session
from webapp.models.sirius.subject import Subject
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@subject_router.delete('/delete/{subject_id}')
async def delete(
    subject_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if not await subject_crud.delete(session, subject_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await redis_remove(Subject.__name__, subject_id)

    return ORJSONResponse(content={'detail': 'Subject deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
