from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.user.router import user_router
from webapp.crud.user import user_crud
from webapp.integrations.cache.cache import redis_drop_key
from webapp.integrations.postgres import get_session
from webapp.models.sirius.user import User
from webapp.utils.auth.jwt import oauth2_scheme


@user_router.delete('/{user_id}')
async def delete_user(
    user_id: int,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> Response:
    if not await user_crud.delete(session, user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await redis_drop_key(User.__name__, user_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
