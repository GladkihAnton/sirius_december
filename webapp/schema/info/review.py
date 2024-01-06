from pydantic import BaseModel


class ReviewInfo(BaseModel):
    user_id: int
    tour_id: int
    rating: float
    comment: str
