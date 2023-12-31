import datetime

from pydantic import BaseModel


class ReservationInfo(BaseModel):
    user_id: int
    tour_id: int
    booking_date: datetime.date
    booking_status: str
