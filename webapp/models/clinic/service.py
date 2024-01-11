from sqlalchemy import Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from webapp.models.meta import DEFAULT_SCHEMA, Base
from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from webapp.models.clinic.doctor import Doctor


class Service(Base):
    __tablename__ = 'service'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, unique=True)

    duration = mapped_column(Time)

    doctors: Mapped[List['Doctor']] = relationship(
        'Doctor',
        secondary=f'{DEFAULT_SCHEMA}.doctor_to_service',
        back_populates='services',
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'duration': self.duration.isoformat()
        }
