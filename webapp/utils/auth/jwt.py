import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Annotated, cast

from fastapi import Depends, Header, HTTPException
from jose import JWTError, jwt
from starlette import status
from typing_extensions import TypedDict

from conf.config import settings
from webapp.models.sirius.user import User, UserRoleEnum


class JwtTokenT(TypedDict):
    uid: str
    exp: datetime
    user_id: int
    role: UserRoleEnum


@dataclass
class JwtAuth:
    secret: str

    def create_token(self, user: User) -> str:
        access_token = {
            'uid': uuid.uuid4().hex,
            'exp': datetime.utcnow() + timedelta(days=6),
            'user_id': user.id,
            'role': user.role.value,
        }
        return jwt.encode(access_token, self.secret)

    def validate_token(self, authorization: Annotated[str, Header()]) -> JwtTokenT:
        _, token = authorization.split()

        try:
            return cast(JwtTokenT, jwt.decode(token, self.secret))
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


jwt_auth = JwtAuth(settings.JWT_SECRET_SALT)


def validate_admin(access_token: JwtTokenT = Depends(jwt_auth.validate_token)) -> JwtTokenT:
    if access_token['role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return access_token

def validate_delivery(access_token: JwtTokenT = Depends(jwt_auth.validate_token)) -> JwtTokenT:
    if access_token['role'] != 'delivery':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return access_token

def validate_customer(access_token: JwtTokenT = Depends(jwt_auth.validate_token)) -> JwtTokenT:
    if access_token['role'] != 'customer':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return access_token
