from pydantic import BaseModel


class ActivityInfo(BaseModel):
    tour_id: int
    title: str
    place: str
    type: str
