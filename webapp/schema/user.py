from pydantic import BaseModel



class UserLogin(BaseModel):
    username: str
    password: str


class UserLoginResponse(BaseModel):
    id: int
    username: str


class UserTokenResponse(BaseModel):
    access_token: str
