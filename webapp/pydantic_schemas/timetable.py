from pydantic import BaseModel
from datetime import datetime, date


class TimetableCreateModel(BaseModel):
    doctor_id: int
    user_id: int
    service_id: int
    start: datetime


class GetHoursResp(BaseModel):
    doctor_id: int = None
    search_date: date
    service_id: int
