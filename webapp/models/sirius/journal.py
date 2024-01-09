from typing import TYPE_CHECKING, List

from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.student import Student
    from webapp.models.sirius.subject import Subject


class Journal(Base):
    __tablename__ = 'journal'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    grade: Mapped[int] = mapped_column(Integer, nullable=True)
    class_date: Mapped[Date] = mapped_column(Date, nullable=False)

    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.subject.id'))
    subject: Mapped[List['Subject']] = relationship(
        'Subject',
        back_populates='records',
    )

    student_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.student.id'))
    student: Mapped[List['Student']] = relationship(
        'Student',
        back_populates='records',
    )
