from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy import Enum as EnumType
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base


class StatusEnum(Enum):
    CREATED = "created"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"


if TYPE_CHECKING:
    from webapp.models.tms.category import Category
    from webapp.models.tms.user import User


class Task(Base):
    __tablename__ = "task"
    __table_args__ = ({"schema": DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )

    title: Mapped[str] = mapped_column(String, nullable=False)

    description: Mapped[str] = mapped_column(String, nullable=False)

    status: Mapped[StatusEnum] = mapped_column(
        EnumType(StatusEnum), nullable=False, default=StatusEnum.CREATED
    )

    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{DEFAULT_SCHEMA}.category.id")
    )

    category: Mapped["Category"] = relationship("Category", back_populates="tasks")

    creator_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{DEFAULT_SCHEMA}.user.id"), nullable=False
    )

    receiver_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{DEFAULT_SCHEMA}.user.id"), nullable=False
    )

    creator: Mapped["User"] = relationship("User", foreign_keys=[creator_id])

    receiver: Mapped["User"] = relationship("User", foreign_keys=[receiver_id])

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
