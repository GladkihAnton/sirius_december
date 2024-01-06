from datetime import date, datetime

from pydantic import BaseModel, field_validator


class ReservationInfo(BaseModel):
    user_id: int
    tour_id: int
    booking_date: date
    booking_status: str

    @field_validator('booking_date')
    @classmethod
    def parse_date(cls, value: date | str) -> date:
        if isinstance(value, date):
            return value
        elif isinstance(value, str):
            try:
                return datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Invalid date format. Use YYYY-MM-DD.')
        raise ValueError('Invalid data type. Expected a string or a date object.')
