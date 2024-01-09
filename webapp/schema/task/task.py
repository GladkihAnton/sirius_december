from pydantic import BaseModel
from datetime import datetime
from webapp.models.tms.task import StatusEnum


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: StatusEnum
    deadline: datetime
    created_at: datetime
    updated_at: datetime


class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: datetime
    category_id: int
    receiver_id: int
