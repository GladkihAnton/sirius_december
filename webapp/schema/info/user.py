from pydantic import BaseModel


class UserInfo(BaseModel):
    username: str
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
