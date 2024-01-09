from typing import TYPE_CHECKING, List

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.group import Group
    from webapp.models.sirius.user import User
    from webapp.models.sirius.journal import Journal


class Student(Base):
    __tablename__ = 'student'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=True)
    birthdate: Mapped[Date] = mapped_column(Date, nullable=False)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.user.id'), unique=True)
    user: Mapped['User'] = relationship(
        'User',
        back_populates='students',
    )

    institution_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.institution.id'))

    group_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.group.id'))
    group: Mapped['Group'] = relationship(
        'Group',
        back_populates='students',
    )

    records: Mapped[List['Journal']] = relationship(
        'Journal',
        back_populates='student',
    )
