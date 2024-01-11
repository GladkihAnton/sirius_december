from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.log_route import LogRoute
from app.db import session
from app.db.crud import get_user
from app.schemas.common import Token
from app.services.token import create_access_token, oauth2_scheme

router = APIRouter(route_class=LogRoute)


@router.post("/info")
async def info(
    access_token: Annotated[str, Depends(oauth2_scheme)],
) -> ORJSONResponse:
    """Получает информацию с использованием предоставленного токена доступа.

    Args:
        access_token (Annotated[str, Depends]): Токен доступа.

    Returns:
        ORJSONResponse: Ответ в формате JSON.
    """
    return ORJSONResponse(access_token)


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(session.get_db),
) -> Token:
    """Аутентификация пользователя и выдача токена доступа.

    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends]): Данные формы для аутентификации.
        session (AsyncSession, optional): Сессия базы данных. Defaults to Depends(session.get_db).

    Returns:
        Token: Модель токена доступа.
    """
    user = await get_user(session, form_data)
    access_token_expires = timedelta(minutes=10)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")
