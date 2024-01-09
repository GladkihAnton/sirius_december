from __future__ import annotations

import uuid
from typing import Any, Type
from sqlalchemy import Column, Text, Float, ForeignKey, Integer, MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped

from app.core.config import Config
from app.services.security import hash_password, verify_password

# Определение метаданных для таблиц
metadata = MetaData(
    schema=Config.SCHEMA_NAME,
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

# Создание базового класса для всех сущностей базы данных
Base: Any = declarative_base(metadata=metadata)

class UUIDMixin:
    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)

class User(Base, UUIDMixin):
    __tablename__ = 'user'
    __table_args__ = {'schema': Config.SCHEMA_NAME}

    username: Mapped[str] = Column(Text, nullable=False, unique=True)
    _hashed_password: Mapped[str] = Column('hashed_password', Text, nullable=False)

    orders: Mapped[list[Type[Order]]] = relationship("Order", back_populates="user")

    @property
    def hashed_password(self):
        return self._hashed_password

    @hashed_password.setter
    def hashed_password(self, plain_password: str):
        self._hashed_password = hash_password(plain_password)

    def check_password(self, plain_password: str) -> bool:
        return verify_password(plain_password, self._hashed_password)

class Order(Base, UUIDMixin):
    __tablename__ = 'order'
    __table_args__ = {'schema': Config.SCHEMA_NAME}

    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey(f"{Config.SCHEMA_NAME}.user.id"), nullable=False)
    user: Mapped[Type[User]] = relationship("User", back_populates="orders")

    products: Mapped[list[Type[OrderProduct]]] = relationship("OrderProduct", back_populates="order")

class Product(Base, UUIDMixin):
    __tablename__ = 'product'
    __table_args__ = {'schema': Config.SCHEMA_NAME}

    name: Mapped[str] = Column(Text, nullable=False, unique=True)
    description: Mapped[str] = Column(Text, nullable=True)
    price: Mapped[float] = Column(Float, nullable=False)

    orders: Mapped[list[Type[OrderProduct]]] = relationship("OrderProduct", back_populates="product")

class OrderProduct(Base):
    __tablename__ = 'order_product'
    __table_args__ = {'schema': Config.SCHEMA_NAME}

    order_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey(f"{Config.SCHEMA_NAME}.order.id"), primary_key=True, nullable=False)
    product_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey(f"{Config.SCHEMA_NAME}.product.id"), primary_key=True, nullable=False)
    quantity: Mapped[int] = Column(Integer, nullable=False)

    order: Mapped[Type[Order]] = relationship("Order", back_populates="products")
    product: Mapped[Type[Product]] = relationship("Product", back_populates="orders")

