from pydantic import BaseModel, ConfigDict


class UserModel(BaseModel):
    tg: str
    address: str

    model_config = ConfigDict(from_attributes=True)
