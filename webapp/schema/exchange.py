from typing import List

from pydantic import BaseModel


class ExchangeData(BaseModel):
    item1_id: int
    item2_id: int


class ExchangeResponse(BaseModel):
    id: int
    item1_id: int
    item2_id: int

class ExchangesResponse(BaseModel):
    exchanges: List[ExchangeResponse]