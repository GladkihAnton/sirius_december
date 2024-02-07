from typing import List

from pydantic import BaseModel, ConfigDict

from webapp.schema.vacation.vacation import Vacation


class EmployeeBase(BaseModel):
    name: str
    user_id: int


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int
    vacations: List[Vacation] = []

    model_config = ConfigDict(from_attributes=True)
