from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.product import Product


class Restaurant(Base):
    __tablename__ = 'restaurant'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String, nullable=False)

    location: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    products: Mapped[List['Product']] = relationship(back_populates='restaurant')
