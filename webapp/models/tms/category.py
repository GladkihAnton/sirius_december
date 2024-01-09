from typing import List, Type

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from webapp.models.meta import DEFAULT_SCHEMA, Base


class Category(Base):
    __tablename__ = 'category'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    description: Mapped[str] = mapped_column(String, nullable=False)

    tasks: Mapped[List["Task"]] = relationship('Task', back_populates='category')

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
