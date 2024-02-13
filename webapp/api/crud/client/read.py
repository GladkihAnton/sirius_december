from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import Annotated
from webapp.utils.auth.jwt import oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm
from webapp.api.crud.client.router import client_router
from webapp.crud.client import client_crud
from webapp.integrations.cache.cache import redis_get, redis_set
from webapp.integrations.postgres import get_session
from webapp.models.sirius.client import Client
from webapp.utils.crud.serializers import serialize_model


@client_router.get('/')
async def get_client(
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    serialized_client = serialize_model(list(await client_crud.get_all(session)))
    return ORJSONResponse({'client': serialized_client})


@client_router.get('/{client_id}')
async def get_cached_client(
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    if cached := (await redis_get(Client.__name__, client_id)):
        return ORJSONResponse({'cached_client': cached})

    client = await client_crud.get_model(session, client_id)

    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_client = serialize_model(client)
    await redis_set(Client.__name__, client_id, serialized_client)

    return ORJSONResponse({'client': serialized_client})