import uuid
from typing import List, Optional, Type

from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

from app.db.models import Order


class UserInfo(BaseModel):
    """Модель данных для создания нового пользователя."""

    username: str = Field(
        min_length=3,
        max_length=20,
        description="Имя пользователя.",
    )
    hashed_password: str = Field(
        description="Хеш пороля пользователя.",
    )
    orders: List[Type[Order]] = Field(default=[], description="Заказы пользователя.")


class ProductInfo(BaseModel):
    """Модель данных для создания нового продукта."""
    id: Optional[UUID] = Field(
        default=uuid.uuid4(),
    )

    name: str = Field(
        min_length=3,
        max_length=50,
        description="Название продукта.",
    )
    description: Optional[str] = Field(
        max_length=255,
        description="Описание продукта.",
    )
    price: float = Field(
        gt=0,
        description="Цена продукта.",
    )


class UserEntity(BaseModel):
    """Модель данных для аутентификации пользователя."""

    username: str = Field(description="Имя пользователя.")
    password: str = Field(description="Пароль пользователя.")


class OrderInfo(BaseModel):
    """Модель данных для создания нового заказа."""

    model_config = ConfigDict(from_attributes=True)
    user_id: Optional[uuid.UUID] = Field(
        description="Идентификатор пользователя.",
    )
    status: Optional[str] = Field(
        description="Статус заказа.",
    )


class UserResponse(BaseModel):
    """Модель данных для ответа с информацией о пользователе."""

    username: str = Field(description="Имя пользователя.")
    orders: List[OrderInfo] = Field(description="Заказы пользователя.")


class OrderProductInfo(BaseModel):
    """Модель данных для добавления продукта в заказ."""

    product_id: uuid.UUID = Field(
        description="Идентификатор продукта.",
    )
    quantity: int = Field(
        gt=0,
        description="Количество продукта.",
    )
