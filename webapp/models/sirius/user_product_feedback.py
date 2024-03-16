import enum
from dataclasses import dataclass
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from .product import Product

class StatusFeedbackEnum(enum.Enum):
    added_to_order = 'added_to_order'
    liked = 'liked'
    disliked = 'disliked'


class UserProductFeedBack(Base):
    __tablename__ = 'user_product_feedback'
    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', name='user_product_unique_feedback'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.user.id'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.product.id'))

    product: Mapped['Product'] = relationship('Product', back_populates='user_product_feedbacks', uselist=False)

    status: Mapped[StatusFeedbackEnum] = mapped_column(ENUM(StatusFeedbackEnum, inherit_schema=True))
