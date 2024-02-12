import enum
from typing import List

from fastapi import Form, UploadFile
from pydantic import BaseModel


class ImageResize(BaseModel):
    file: UploadFile

class FillQueue(BaseModel):
    user_ids: List[int]


class ResizeStatusEnum(enum.Enum):
    status = 'status'


class ImageResizeResponse(BaseModel):
    status: ResizeStatusEnum
    task_id: str
