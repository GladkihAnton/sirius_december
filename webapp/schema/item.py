from typing import List

from pydantic import BaseModel


ITEM_TABLE = 'item'


class ItemData(BaseModel):
    title: str
    exchanges: List[int] = []  # Идентификаторы обменов


class ItemTitle(BaseModel):
    title: str


class ItemExchanges(BaseModel):
    exchanges: List[int]


class ItemExchange(BaseModel):
    exchange: int


class ItemId(BaseModel):
    id: int


class ItemResponse(BaseModel):
    id: int
    title: str
    exchanges: List[int]  # Идентификаторы обменов


class ItemsResponse(BaseModel):
    items: List[ItemResponse]
