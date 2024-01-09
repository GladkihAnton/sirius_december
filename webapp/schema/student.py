from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from webapp.schema.user import UserRead


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    surname: Optional[str] = None
    birthdate: date

    @field_validator('birthdate')
    @classmethod
    def parse_birthdate(cls, value: str | date) -> date:
        if isinstance(value, date):
            return value
        elif isinstance(value, str):
            return datetime.strptime(value, '%Y-%m-%d').date()
        raise ValueError('Invalid type. Must be string or date.')


class StudentInfo(StudentBase):
    user_id: int
    institution_id: int
    group_id: int


class StudentRead(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user: UserRead
