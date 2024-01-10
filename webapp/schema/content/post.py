# проверка данных, сериализация/десериализация
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    content: str


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    content: Optional[str] = None
