from datetime import timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from conf.config import settings
from webapp.api.auth.router import auth_router
from webapp.integrations.postgres import get_session
from webapp.schema.auth.token import Token
from webapp.utils.auth.jwt import authenticate_user, create_access_token, oauth2_scheme


@auth_router.post('/info')
async def info(
    access_token: Annotated[str, Depends(oauth2_scheme)],
) -> ORJSONResponse:
    return ORJSONResponse(access_token)


@auth_router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
) -> Token:
    user = await authenticate_user(session, form_data)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type='bearer')
