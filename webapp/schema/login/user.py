from pydantic import BaseModel


class UserLogin(BaseModel):
    username: int
    code: str


class UserLoginResponse(BaseModel):
    access_token: str
