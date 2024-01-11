from datetime import datetime, timedelta
from typing import Any

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.core.config import Config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="sirius/api/v1/token/login")


def create_access_token(data: dict[str, Any], expires_delta: timedelta) -> str:
    """Создает токен доступа на основе предоставленных данных и времени истечения.

    Args:
        data (dict[str, Any]): Словарь данных, которые будут закодированы в токене.
        expires_delta (timedelta): Время, на которое будет установлен срок действия токена.

    Returns:
        str: Закодированный токен доступа.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SALT, algorithm=Config.ALGORITHM)
    return encoded_jwt
