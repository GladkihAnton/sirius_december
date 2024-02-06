from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    role: Optional[str]
    additional_info: Optional[dict]


class UserLogin(BaseModel):
    username: str
    password: str

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'username': 'admin1',
                    'password': 'qwerty',
                }
            ]
        }
    }


class UserLoginResponse(BaseModel):
    access_token: str

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
                }
            ]
        }
    }


class UserCreate(User):
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'examples': [
                {
                    'username': 'user',
                    'email': 'user@example.com',
                    'role': 'admin',
                    'additional_info': {'full_name': 'Дмитрий Петров'},
                    'password': 'qwerty',
                }
            ]
        },
    )


class UserRead(User):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'examples': [
                {
                    'id': 1,
                }
            ]
        },
    )
