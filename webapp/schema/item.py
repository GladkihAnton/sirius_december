from typing import List

from pydantic import BaseModel


class ItemData(BaseModel):
    name: str


class ItemResponse(BaseModel):
    id: int
    name: str


class ItemsResponse(BaseModel):
    items: List[ItemResponse]