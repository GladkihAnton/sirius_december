from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.subject import Subject
    from webapp.models.sirius.teacher import Teacher


class Institution(Base):
    __tablename__ = 'institution'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, unique=True)
    phone: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    teachers: Mapped[List['Teacher']] = relationship(
        'Teacher',
        back_populates='institution',
    )

    subjects: Mapped[List['Subject']] = relationship(
        'Subject',
        back_populates='institution',
    )
