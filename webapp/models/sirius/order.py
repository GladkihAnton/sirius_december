from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.product import Product
    from webapp.models.sirius.user import User


class Order(Base):
    __tablename__ = 'order'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    restaurant_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.restaurant.id'), nullable=False)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.user.id'), nullable=False)

    create: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    where_to_deliver: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped['User'] = relationship(back_populates='orders')

    products: Mapped[List['Product']] = relationship(
        secondary=f'{DEFAULT_SCHEMA}.order_product',
        back_populates='orders',
    )
