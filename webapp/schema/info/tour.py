import datetime

from pydantic import BaseModel


class TourInfo(BaseModel):
    title: str
    price: float
    start_date: datetime.date
    end_date: datetime.date
