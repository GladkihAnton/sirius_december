from sqlalchemy import Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base


class User(Base, AsyncAttrs):
    __tablename__ = 'user'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    username: Mapped[str] = mapped_column(String, unique=True)

    role: Mapped[str] = mapped_column(String, default='staff')

    hashed_password: Mapped[str] = mapped_column(String)

    # Связь с Employee
    employee = relationship('Employee', uselist=False, back_populates='user')
