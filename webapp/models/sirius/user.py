from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.student import Student
    from webapp.models.sirius.teacher import Teacher


class User(Base):
    __tablename__ = 'user'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)

    teachers: Mapped[List['Teacher']] = relationship(
        'Teacher',
        back_populates='user',
    )

    students: Mapped[List['Student']] = relationship(
        'Student',
        back_populates='user',
    )
