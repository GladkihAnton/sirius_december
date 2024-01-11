from pydantic import BaseModel, EmailStr, Field


class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, json_schema_extra='username')
    email: EmailStr = Field(..., json_schema_extra='user@example.com')
    password: str = Field(..., min_length=8, json_schema_extra='yourpassword')

    class ConfigDict:
        schema_extra = {
            'example': {
                'username': 'username',
                'email': 'user@example.com',
                'password': 'yourpassword',
            }
        }
