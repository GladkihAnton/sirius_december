from pydantic import BaseModel, ConfigDict


class ActivityInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tour_id: int
    title: str
    place: str
    type: str
