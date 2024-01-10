import orjson
import redis.asyncio as aioredis
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.crud.user import get_user_by_id
from webapp.db.postgres import get_session
from webapp.on_startup.redis import get_redis_pool
from webapp.schema.login.user import User
from webapp.utils.auth.jwt import jwt_auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
    redis: aioredis.Redis = Depends(get_redis_pool),
) -> User:
    jwt_payload = jwt_auth.validate_token(token)
    user_id = jwt_payload['user_id']

    # Попытка получить данные пользователя из Redis
    cached_user_data = await redis.get(f'user_{user_id}')
    if cached_user_data:
        # Десериализация данных пользователя из кэша
        user_data = orjson.loads(cached_user_data)
        print(user_data)
        return User.model_validate(user_data)

    # Получение данных пользователя из базы данных
    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found'
        )

    # Сериализация и сохранение данных пользователя в Redis
    await redis.set(f'user_{user_id}', orjson.dumps(user.dict()), ex=3600)

    return user