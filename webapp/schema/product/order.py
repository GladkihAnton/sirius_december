from pydantic import BaseModel


class PostOrderModel(BaseModel):
    product_id: int
