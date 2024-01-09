from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.user.router import user_router
from webapp.crud.user import user_crud
from webapp.integrations.cache.cache import redis_drop_key
from webapp.integrations.postgres import get_session
from webapp.models.sirius.user import User
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@user_router.post('/delete/{user_id}')
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if not await user_crud.delete(session, user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await redis_drop_key(User.__name__, user_id)
    return ORJSONResponse(content={'message': 'User removed successfully'}, status_code=status.HTTP_204_NO_CONTENT)
