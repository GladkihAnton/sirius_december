from pydantic import BaseModel, ConfigDict
from datetime import time


class ServiceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    duration: time


class ServiceCreateModel(BaseModel):
    name: str
    duration: time