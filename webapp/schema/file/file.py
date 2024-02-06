from datetime import datetime

from pydantic import BaseModel, ConfigDict


class File(BaseModel):
    lesson_id: int
    type: str
    description: str
    content_type: str
    size: int

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'lesson_id': 1,
                    'type': 'video',
                    'description': 'Видеоурок по основам Python.',
                    'content_type': 'video/mp4',
                    'size': 2048,
                }
            ]
        }
    }


class FileCreate(File):
    pass

    model_config = ConfigDict(from_attributes=True)


class FileRead(File):
    id: int
    minio_path: str
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)
