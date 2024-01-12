from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from webapp.models.tms.task import StatusEnum


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    status: StatusEnum
    deadline: datetime
    creator_id: int
    receiver_id: int
    created_at: datetime
    updated_at: datetime


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    deadline: Optional[datetime] = None
    category_id: Optional[int] = None
    receiver_id: Optional[int] = None


class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: datetime
    category_id: int
    receiver_id: int
