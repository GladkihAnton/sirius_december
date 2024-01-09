from sqlalchemy import ForeignKey, UniqueConstraint
from webapp.models.meta import DEFAULT_SCHEMA, Base
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from webapp.models.meta import DEFAULT_SCHEMA, Base


class DoctorToService(Base):
    __tablename__ = 'doctor_to_service'
    __table_args__ = (
        {'schema': DEFAULT_SCHEMA},
        #UniqueConstraint('doctor_id', 'service_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    doctor_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.doctor.id'))

    service_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.service.id'))

