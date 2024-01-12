from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from webapp.schema.subject import SubjectBase


class JournalBase(BaseModel):
    grade: Optional[int]
    class_date: date

    @field_validator('class_date')
    @classmethod
    def parse_date(cls, value: str | date) -> date:
        if isinstance(value, date):
            return value
        elif isinstance(value, str):
            return datetime.strptime(value, '%Y-%m-%d').date()
        raise ValueError('Invalid type. Must be string or date.')


class JournalInfo(JournalBase):
    subject_id: int
    student_id: int


class JournalData(JournalBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class SubjectWithJournal(SubjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    records: List[JournalData]


class StudentsJournal(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    surname: Optional[str] = None
    birthdate: date
    subjects: List[SubjectWithJournal]

    @field_validator('birthdate')
    @classmethod
    def parse_birthdate(cls, value: str | date) -> date:
        if isinstance(value, date):
            return value
        elif isinstance(value, str):
            return datetime.strptime(value, '%Y-%m-%d').date()
        raise ValueError('Invalid type. Must be string or date.')


"""
[
    {
        id,
        first_name,
        last_name,
        surname,
        birthdate,
        subjects: [
            {
                id,
                title,
                records: [
                    {
                        id,
                        grade,
                        class_date
                    }
                ]
            }
        ]
    }
]
"""
