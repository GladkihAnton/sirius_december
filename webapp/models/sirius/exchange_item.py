from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from webapp.models.meta import DEFAULT_SCHEMA, Base


class ExchangeItem(Base):
    __tablename__ = 'exchange_item'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    exchange_id: Mapped[int] = mapped_column(Integer, ForeignKey(f"{DEFAULT_SCHEMA}.exchange.id"), primary_key=True)

    item_id: Mapped[int] = mapped_column(Integer, ForeignKey(f"{DEFAULT_SCHEMA}.item.id"), primary_key=True)
