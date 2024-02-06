from sqlalchemy import Boolean, Date, ForeignKey, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base


class Vacation(Base, AsyncAttrs):
    __tablename__ = 'vacation'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    start_date: Mapped[Date] = mapped_column(Date)

    end_date: Mapped[Date] = mapped_column(Date)

    approved: Mapped[Boolean] = mapped_column(
        Boolean, nullable=True, default=None
    )

    employee_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f'{DEFAULT_SCHEMA}.employee.id')
    )

    # Связь с Employee
    employee = relationship('Employee', back_populates='vacations')
