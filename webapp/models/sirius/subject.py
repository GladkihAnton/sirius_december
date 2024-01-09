from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.group import Group
    from webapp.models.sirius.institution import Institution
    from webapp.models.sirius.teacher import Teacher
    from webapp.models.sirius.journal import Journal


class Subject(Base):
    __tablename__ = 'subject'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)

    institution_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.institution.id'))
    institution: Mapped['Institution'] = relationship(
        'Institution',
        back_populates='subjects',
    )

    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.teacher.id'))
    teacher: Mapped['Teacher'] = relationship(
        'Teacher',
        back_populates='subjects',
    )

    groups: Mapped[List['Group']] = relationship(
        'Group',
        secondary=f'{DEFAULT_SCHEMA}.group_subject',
        back_populates='subjects',
    )

    records: Mapped[List['Journal']] = relationship(
        'Journal',
        back_populates='subject',
    )
