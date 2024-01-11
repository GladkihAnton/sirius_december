from pydantic import BaseModel, field_validator

from webapp.schema.crud import IdField
from webapp.utils.auth.password import hash_password


class UserDTO(BaseModel):
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def hash_password(cls, v: str) -> str:
        return hash_password(v)


class UserResponse(IdField):
    username: str
