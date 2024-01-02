from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.user.router import user_router
from webapp.api.crud.user.utils.get_user import get_user_model
from webapp.crud.user import user_crud
from webapp.integrations.cache.cache import redis_get, redis_set
from webapp.integrations.postgres import get_session
from webapp.models.sirius.user import User
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth
from webapp.utils.crud.serializers import serialize_model


@user_router.get('/')
async def get_users(
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    serialized_users = serialize_model(list(await user_crud.get_all(session)))
    return ORJSONResponse({'users': serialized_users})


@user_router.get('/{user_id}')
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if cached := (await redis_get(User.__name__, user_id)):
        return ORJSONResponse({'cached_user': cached})

    user = await get_user_model(session, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_user = serialize_model(user)
    await redis_set(User.__name__, user_id, serialized_user)

    return ORJSONResponse({'user': serialized_user})
