from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    username: Mapped[int] = mapped_column(BigInteger, unique=True)
    code: Mapped[str] = mapped_column(String)
