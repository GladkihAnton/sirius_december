from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import Annotated
from webapp.api.crud.client.router import client_router
from webapp.crud.client import client_crud
from webapp.integrations.postgres import get_session
from webapp.schema.info.client import ClientInfo
from fastapi.security import OAuth2PasswordRequestForm

from webapp.utils.auth.jwt import oauth2_scheme


@client_router.post('/update/{client_id}')
async def update_client(
    body: ClientInfo,
    client_id: int,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    exists = client_crud.get_model(session, client_id) is not None

    await client_crud.update(session, client_id, body)

    if exists:
        return ORJSONResponse(
            content={'message': 'Client updated successfully'}, status_code=status.HTTP_200_OK
        )

    return ORJSONResponse(content={'message': 'Client created successfully'}, status_code=status.HTTP_201_CREATED)
