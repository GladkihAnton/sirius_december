from pydantic import BaseModel, ConfigDict, Field

from webapp.schema.product.base import ProductModel
from webapp.schema.user.base import UserModel


class OrderModel(BaseModel):
    user: UserModel

    product: ProductModel

    model_config = ConfigDict(from_attributes=True)

