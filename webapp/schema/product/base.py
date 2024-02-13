from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductModel(BaseModel):
    id: int

    offer: str

    title: str

    url: str

    picture_url: str

    price: float

    model_config = ConfigDict(from_attributes=True)
