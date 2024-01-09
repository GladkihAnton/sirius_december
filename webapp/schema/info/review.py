from pydantic import BaseModel, ConfigDict


class ReviewInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    tour_id: int
    rating: float
    comment: str
