# проверка данных, сериализация/десериализация
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
