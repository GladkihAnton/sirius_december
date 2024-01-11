from typing import List

from pydantic import BaseModel


EXCHANGE_TABLE = 'exchange'


class ExchangeData(BaseModel):
    title: str


class ExchangeResponse(BaseModel):
    id: int
    title: str
    items: List[int]  # Идентификаторы товаров


class ExchangesResponse(BaseModel):
    exchanges: List[ExchangeResponse]
