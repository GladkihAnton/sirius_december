import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Annotated, cast

from fastapi import Header, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from starlette import status
from typing_extensions import TypedDict

from conf.config import settings

auth_scheme = HTTPBearer()


class JwtTokenT(TypedDict):
    uid: str
    exp: datetime
    user_id: int
    role: str


@dataclass
class JwtAuth:
    secret: str

    def create_token(self, user_id: int, role: str) -> str:
        access_token = {
            'uid': uuid.uuid4().hex,
            'exp': datetime.utcnow() + timedelta(days=6),
            'user_id': user_id,
            'role': role,
        }
        return jwt.encode(access_token, self.secret)

    def validate_token(self, authorization: Annotated[str, Header()]) -> JwtTokenT:
        _, token = authorization.split()

        try:
            return cast(JwtTokenT, jwt.decode(token, self.secret))
        except JWTError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    def get_current_user(self, credentials: HTTPAuthorizationCredentials = Security(auth_scheme)) -> JwtTokenT:
        return self.validate_token(credentials.credentials)


jwt_auth = JwtAuth(settings.JWT_SECRET_SALT)
