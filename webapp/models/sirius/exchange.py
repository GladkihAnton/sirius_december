from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from webapp.models.meta import DEFAULT_SCHEMA, Base
from webapp.models.sirius.exchange_to_item import exchange_to_item


class Exchange(Base):
    __tablename__ = 'exchange'
    __table_args__ = {'schema': DEFAULT_SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String, unique=True)

    items: Mapped[List["Item"]] = relationship(secondary=exchange_to_item, back_populates='exchanges')
