from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class JournalInfo(BaseModel):
    grade: Optional[int]
    class_date: date
    subject_id: int
    student_id: int

    @field_validator('class_date')
    @classmethod
    def parse_date(cls, value: str | date) -> date:
        if isinstance(value, date):
            return value
        elif isinstance(value, str):
            return datetime.strptime(value, '%Y-%m-%d').date()
        raise ValueError('Invalid type. Must be string or date.')
