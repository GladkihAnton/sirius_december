from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.institution import Institution
    from webapp.models.sirius.subject import Subject
    from webapp.models.sirius.user import User


class Teacher(Base):
    __tablename__ = 'teacher'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String, nullable=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.user.id'), unique=True)
    user: Mapped['User'] = relationship(
        'User',
        back_populates='teachers',
    )

    subjects: Mapped[List['Subject']] = relationship(
        'Subject',
        back_populates='teacher',
    )

    institution_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.institution.id'))
    institution: Mapped[List['Institution']] = relationship(
        'Institution',
        back_populates='teachers',
    )
