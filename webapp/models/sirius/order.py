import enum

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from webapp.models.meta import DEFAULT_SCHEMA, Base


class OrderEnum(enum.Enum):
    success = 'success'
    failed = 'failed'
    pending = 'pending'


class Order(Base):
    __tablename__ = 'order'
    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', name='user_product_unique'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.user.id'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.product.id'))

    status: Mapped[OrderEnum] = mapped_column(ENUM(OrderEnum, inherit_schema=True), default=OrderEnum.pending)
