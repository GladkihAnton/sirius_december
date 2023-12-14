import enum

from fastapi import Form, UploadFile
from pydantic import BaseModel


class ImageResize(BaseModel):
    image: UploadFile

    width: int = Form()
    height: int = Form()


class ResizeStatusEnum(enum.Enum):
    status = 'status'


class ImageResizeResponse(BaseModel):
    status: ResizeStatusEnum
    task_id: str
