from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.auth.router import auth_router
from webapp.crud.user import get_user
from webapp.integrations.postgres import get_session
from datetime import timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from conf.config import settings
from webapp.api.auth.router import auth_router
from webapp.integrations.postgres import get_session
from webapp.utils.auth.jwt import authenticate_user, create_access_token, oauth2_scheme
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

@auth_router.post('/login', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], #Получаем данные формы запроса аутентификации
    session: AsyncSession = Depends(get_session), #Получаем сессию бд через установку зависимости (Depends) от get_session
) -> Token:
    user = await authenticate_user(session, form_data)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type='bearer')