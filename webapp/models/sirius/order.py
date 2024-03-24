import enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.product import Product
    from webapp.models.sirius.user import User


class OrderEnum(enum.Enum):
    success = 'success'
    failed = 'failed'
    pending = 'pending'


class Order(Base):
    __tablename__ = 'order'
    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', name='user_product_unique_order'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.user.id'))
    user: Mapped['User'] = relationship('User', back_populates='orders', uselist=False)

    product_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.product.id'))
    product: Mapped['Product'] = relationship('Product', back_populates='orders', uselist=False)

    status: Mapped[OrderEnum] = mapped_column(ENUM(OrderEnum, inherit_schema=True), default=OrderEnum.pending)
