from typing import List

from pydantic import BaseModel, ConfigDict


class OPInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    order_id: int
    product_id: int
    quantity: int


class OPResponse(BaseModel):
    order_id: int
    product_id: int
    quantity: int


class OPsListResponse(BaseModel):
    products: List[OPResponse]
