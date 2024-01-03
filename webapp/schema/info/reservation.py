from pydantic import BaseModel


class ReservationInfo(BaseModel):
    user_id: int
    tour_id: int
    booking_date: str
    booking_status: str
