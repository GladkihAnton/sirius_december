from typing import List, Optional

from pydantic import BaseModel


class RestaurantsList(BaseModel):
    # TODO Хз насколько это правильно
    name: str


class RestaurantInfo(BaseModel):
    id: int
    name: str
    location: str


class RestaurantsListResponse(BaseModel):
    # TODO Хз насколько это правильно
    r_list: List[RestaurantInfo]
