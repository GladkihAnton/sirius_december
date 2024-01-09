from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from webapp.models.meta import DEFAULT_SCHEMA, Base
from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from webapp.models.clinic.service import Service


class Doctor(Base):
    __tablename__ = 'doctor'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

    specialization: Mapped[str] = mapped_column(String)

    first_name: Mapped[str] = mapped_column(String)

    last_name: Mapped[str] = mapped_column(String)

    services: Mapped[List['Service']] = relationship(
        'Service',
        secondary=f'{DEFAULT_SCHEMA}.doctor_to_service',
        back_populates='doctors',
    )
