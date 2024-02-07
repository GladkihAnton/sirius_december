from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.client.router import client_router
from webapp.crud.client import client_crud
from webapp.integrations.postgres import get_session
from fastapi.security import OAuth2PasswordRequestForm

from webapp.utils.auth.jwt import oauth2_scheme
from typing import Annotated

@client_router.post('/delete/{client_id}')
async def delete_client(
    client_id: int,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    if not await client_crud.delete(session, client_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(content={'message': 'Client removed successfully'}, status_code=status.HTTP_204_NO_CONTENT)
