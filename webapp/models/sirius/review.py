from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.tour import Tour


class Review(Base):
    __tablename__ = 'review'
    __table_args__ = {'schema': DEFAULT_SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.user.id'))

    tour_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.tour.id'))

    rating: Mapped[float] = mapped_column(DECIMAL(3, 2))

    comment: Mapped[str] = mapped_column(String)

    posted: Mapped[str] = mapped_column(Date)

    tour: Mapped['Tour'] = relationship('Tour', back_populates='reviews')
