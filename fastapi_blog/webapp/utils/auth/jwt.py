# создание и проверка токена аутентификации JSON Web Token (JWT)

import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Annotated, cast

from fastapi import Header, HTTPException
from jose import JWTError, jwt
from starlette import status
from typing_extensions import TypedDict

from conf.config import settings


class JwtTokenT(TypedDict):
    uid: int
    exp: datetime
    user_id: int


@dataclass
class JwtAuth:
    secret: str

    # принимает идентификатор пользователя в качестве параметра и возвращает JWT-токен, содержащий идентификатор пользователя и срок действия токена
    def create_token(self, user_id: int) -> str:
        access_token = {
            'uid': uuid.uuid4().hex,
            'exp': datetime.utcnow() + timedelta(days=1),
            'user_id': user_id,
        }
        return jwt.encode(access_token, self.secret)
    
    # принимает заголовок Authorization, содержащий токен, и проверяет его подлинность
    def validate_token(self, authorization: Annotated[str, Header()]) -> JwtTokenT:
        _, token = authorization.split()

        try:
            return cast(JwtTokenT, jwt.decode(token, self.secret))
        except JWTError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

# объект jwt_auth создается с использованием секретного ключа, определенного в файле конфигурации settings
jwt_auth = JwtAuth(settings.JWT_SECRET_SALT)
