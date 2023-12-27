from typing import TYPE_CHECKING, List

from sqlalchemy import DECIMAL, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.activity import Activity
    from webapp.models.sirius.review import Review


class Tour(Base):
    __tablename__ = 'tour'
    __table_args__ = {'schema': DEFAULT_SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String, unique=True)

    price: Mapped[float] = mapped_column(DECIMAL(10, 2))

    start_date: Mapped[str] = mapped_column(Date)

    end_date: Mapped[str] = mapped_column(Date)

    activity: Mapped[List['Activity']] = relationship('Activity', back_populates='tour')

    reviews: Mapped[List['Review']] = relationship('Review', back_populates='tour')
