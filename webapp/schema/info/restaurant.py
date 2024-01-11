from typing import List

from pydantic import BaseModel, ConfigDict


class RestaurantInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    location: str


class RestaurantResponse(BaseModel):
    id: int
    name: str
    location: str


class RestaurantsListResponse(BaseModel):
    restaurants: List[RestaurantResponse]


class RestaurantSearch(BaseModel):
    name: str | None
