from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.user.router import user_router
from webapp.crud.user import user_crud
from webapp.integrations.cache.cache import redis_get, redis_set
from webapp.integrations.postgres import get_session
from webapp.models.sirius.user import User
from webapp.utils.auth.jwt import oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm
from webapp.utils.crud.serializers import serialize_model
from typing import Annotated


@user_router.get('/')
async def get_users(
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    serialized_users = serialize_model(list(await user_crud.get_all(session)))
    return ORJSONResponse({'users': serialized_users})


@user_router.get('/{id}')
async def get_cached_user(
    id: int,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    if cached := (await redis_get(User.__name__, id)):
        return ORJSONResponse({'cached_user': cached})

    user = await user_crud.get_model(session, id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_user = serialize_model(user)
    await redis_set(User.__name__, id, serialized_user)

    return ORJSONResponse({'user': serialized_user})
