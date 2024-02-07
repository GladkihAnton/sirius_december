from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class VacationBase(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
    approved: Optional[bool] = None
    employee_id: int


class VacationCreate(VacationBase):
    pass


class VacationRequst(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class VacationUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    approved: Optional[bool] = None


class Vacation(VacationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
