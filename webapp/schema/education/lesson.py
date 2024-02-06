from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Lesson(BaseModel):
    title: str
    content: str
    order: int

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'title': 'Введение в Python',
                    'content': 'Этот урок познакомит вас с основами Python.',
                    'order': 1,
                }
            ]
        }
    }


class LessonCreate(Lesson):
    pass

    model_config = ConfigDict(from_attributes=True)


class LessonRead(Lesson):
    id: int
    course_id: int
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)
