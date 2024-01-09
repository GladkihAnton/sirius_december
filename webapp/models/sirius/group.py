from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.student import Student
    from webapp.models.sirius.subject import Subject


class Group(Base):
    __tablename__ = 'group'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)

    institution_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.institution.id'))

    students: Mapped[List['Student']] = relationship(
        'Student',
        back_populates='group',
    )

    subjects: Mapped[List['Subject']] = relationship(
        'Subject',
        secondary=f'{DEFAULT_SCHEMA}.group_subject',
        back_populates='groups',
    )
