from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    post_id: int
    created_at: datetime


class CommentUpdate(BaseModel):
    content: Optional[str] = None