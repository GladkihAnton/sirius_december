import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import cast

from fastapi import HTTPException
from jose import JWTError, jwt
from starlette import status
from typing_extensions import TypedDict

from conf.config import settings


class JwtTokenT(TypedDict):
    uid: str
    exp: datetime
    user_id: int


@dataclass
class JwtAuth:
    secret: str

    def create_token(self, user_id: int) -> str:
        token = {
            'uid': uuid.uuid4().hex,
            'exp': datetime.utcnow() + timedelta(days=6),
            'user_id': user_id,
        }
        return jwt.encode(token, self.secret)

    def validate_token(self, access_token: str) -> JwtTokenT:

        try:
            return cast(JwtTokenT, jwt.decode(access_token, self.secret))
        except JWTError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


jwt_auth = JwtAuth(settings.JWT_SECRET_SALT)
