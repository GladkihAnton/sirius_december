import datetime as dt
import enum
import uuid
from typing import Optional, Union, Type

from app.db.models import Order
from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt


class UserInfo(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=20,
        description="Имя пользователя.",
    )
    hashed_password: str = Field(
        description="Хеш пороля пользователя.",
    )
    orders: list[Type[Order]] = Field(
        default=[],
        description="Заказы пользователя."
    )

class UserEntity(BaseModel):
    username: str = Field(
        description="Имя пользователя."
    )
    password: str = Field(
        description="Пароль пользователя."
    )

class UserResponse(BaseModel):
    username: str = Field(
        description="Имя пользователя."
    )
    orders: list[Type[Order]] = Field(
        default=[],
        description="Заказы пользователя."
    )