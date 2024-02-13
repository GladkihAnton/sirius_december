from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.client.router import client_router
from webapp.crud.client import client_crud
from webapp.integrations.postgres import get_session
from webapp.schema.info.client import ClientInfo
from webapp.utils.auth.jwt import oauth2_scheme

@client_router.post('/create')
async def create_client(
    body: ClientInfo,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    try:
        await client_crud.create(session, body)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={'message': 'client created successfully'}, status_code=status.HTTP_201_CREATED)