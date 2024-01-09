from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.client.router import client_router
from webapp.crud.client import client_crud
from webapp.integrations.postgres import get_session
from webapp.schema.info.client import ClientInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@client_router.post('/update/{client_id}')
async def update_client(
    body: ClientInfo,
    client_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    exists = client_crud.get_model(session, client_id) is not None

    await client_crud.update(session, client_id, body)

    if exists:
        return ORJSONResponse(
            content={'message': 'Client updated successfully'}, status_code=status.HTTP_204_NO_CONTENT
        )

    return ORJSONResponse(content={'message': 'Client created successfully'}, status_code=status.HTTP_201_CREATED)
