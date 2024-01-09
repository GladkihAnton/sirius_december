from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserInfo(UserBase):
    password: str


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserLoginResponse(BaseModel):
    access_token: str
