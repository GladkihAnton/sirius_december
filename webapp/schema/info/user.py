from pydantic import BaseModel, ConfigDict


class UserInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
