from typing import List

from pydantic import BaseModel


class RestaurantsListRequest(BaseModel):
    # TODO Хз насколько это правильно
    name: str


class RestaurantsListResponse(BaseModel):
    # TODO Хз насколько это правильно
    r_list: List[str]
