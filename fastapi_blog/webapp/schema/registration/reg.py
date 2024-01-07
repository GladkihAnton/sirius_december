# эндпоинт на регистрацию пользователя
from pydantic import BaseModel, EmailStr, Field


class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, example='username')
    email: EmailStr = Field(..., example='user@example.com')
    password: str = Field(..., min_length=8, example='yourpassword')

    class Config:
        schema_extra = {'example': {'username': 'username', 'email': 'user@example.com', 'password': 'yourpassword'}}
