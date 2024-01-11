from typing import List

from pydantic import BaseModel


ITEM_TABLE = 'item'


class ItemData(BaseModel):
    title: str
    exchanges: List[int] = []  # Идентификаторы обменов


class ItemResponse(BaseModel):
    id: int
    title: str
    exchanges: List[int]  # Идентификаторы обменов


class ItemsResponse(BaseModel):
    items: List[ItemResponse]
