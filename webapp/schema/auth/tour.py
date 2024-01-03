from pydantic import BaseModel


class TourInfo(BaseModel):
    title: str
    price: float
    start_date: str
    end_date: str
