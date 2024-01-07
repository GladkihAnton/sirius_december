from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.crud.user import get_user_by_id
from webapp.db.postgres import get_session
from webapp.schema.login.user import User
from webapp.utils.auth.jwt import jwt_auth

# получение текущего пользователя с помощью токена аутентификации OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# проверка подлинности пользователя
async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> User:
    jwt_payload = jwt_auth.validate_token(token)
    user_id = jwt_payload['user_id']
    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user
