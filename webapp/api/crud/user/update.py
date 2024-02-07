from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.user.router import user_router
from webapp.crud.user import user_crud
from webapp.integrations.postgres import get_session
from webapp.schema.info.user import UserInfo
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from webapp.utils.auth.jwt import oauth2_scheme


@user_router.post('/update/{id}')
async def update_user(
    body: UserInfo,
    id: int,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    exists = user_crud.get_model(session, id) is not None

    await user_crud.update(session, id, body)

    if exists:
        return ORJSONResponse(content={'message': 'User updated successfully'}, status_code=status.HTTP_204_NO_CONTENT)
    return ORJSONResponse(content={'message': 'User created successfully'}, status_code=status.HTTP_201_CREATED)
