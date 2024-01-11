from typing import List

from pydantic import BaseModel, ConfigDict


class OrderInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    restaurant_id: int
    user_id: int
    where_to_deliver: str


class OrderResponse(BaseModel):
    restaurant_id: int
    user_id: int
    where_to_deliver: str


class OrdersListResponse(BaseModel):
    products: List[OrderResponse]
