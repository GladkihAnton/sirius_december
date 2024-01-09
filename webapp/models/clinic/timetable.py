from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from webapp.models.meta import DEFAULT_SCHEMA, Base
from datetime import datetime


class Timetable(Base):
    __tablename__ = 'timetable'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    doctor_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.doctor.id'))

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.user.id'))

    service_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.service.id'))

    start: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
