from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    content: str


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    created_at: datetime


class PostUpdate(BaseModel):
    content: Optional[str] = None