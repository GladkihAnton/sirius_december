from sqlalchemy import Integer, String, Column, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

from webapp.models.meta import DEFAULT_SCHEMA, Base

exchange_to_item = Table(
    "exchange_to_item",
    Base.metadata,
    Column("exchange_id", ForeignKey(f"{DEFAULT_SCHEMA}.exchange.id"), primary_key=True),
    Column("item_id", ForeignKey(f"{DEFAULT_SCHEMA}.item.id"), primary_key=True),
    schema=DEFAULT_SCHEMA,
)
