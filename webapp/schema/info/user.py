from typing import List

from pydantic import BaseModel, ConfigDict


class UserInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    hashed_password: str


class UserResponse(BaseModel):
    username: str
    password: str


class UserListResponse(BaseModel):
    users: List[UserResponse]


class UserLoginResponse(BaseModel):
    access_token: str


class UserLogin(BaseModel):
    username: str
    password: str
