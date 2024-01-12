from typing import TYPE_CHECKING, List

from sqlalchemy import Float, ForeignKey, Integer, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.order import Order
    from webapp.models.sirius.restaurant import Restaurant


class Product(Base):
    __tablename__ = 'product'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    restaurant_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.restaurant.id'), nullable=False)

    name: Mapped[str] = mapped_column(String, nullable=False)

    price: Mapped[float] = mapped_column(Float, nullable=False)

    restaurant: Mapped['Restaurant'] = relationship(back_populates='products')

    orders: Mapped[List['Order']] = relationship(
        secondary=f'{DEFAULT_SCHEMA}.order_product',
        back_populates='products',
    )


product_index = Index('product_index', Product.name, postgresql_using='btree')
