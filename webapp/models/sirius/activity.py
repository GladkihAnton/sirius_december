from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.tour import Tour


class Activity(Base):
    __tablename__ = 'activity'
    __table_args__ = {'schema': DEFAULT_SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    tour_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.tour.id'))

    title: Mapped[str] = mapped_column(String)

    place: Mapped[str] = mapped_column(String)

    type: Mapped[str] = mapped_column(String)

    tour: Mapped['Tour'] = relationship('Tour', back_populates='activity')
