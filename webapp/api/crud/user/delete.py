from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import Annotated
from webapp.api.crud.user.router import user_router
from webapp.crud.user import user_crud
from webapp.integrations.postgres import get_session
from webapp.utils.auth.jwt import oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


@user_router.post('/delete/{id}')
async def delete_user(
    id: int,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    if not await user_crud.delete(session, id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(content={'message': 'User removed successfully'}, status_code=status.HTTP_204_NO_CONTENT)
