from typing import List

from pydantic import BaseModel, ConfigDict


class ProductInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    restaurant_id: int
    price: float


class ProductResponse(BaseModel):
    name: str
    restaurant_id: int
    price: float


class ProductsListResponse(BaseModel):
    products: List[ProductResponse]
