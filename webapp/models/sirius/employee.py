from typing import List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base
from webapp.models.sirius.user import User
from webapp.models.sirius.vacation import Vacation


class Employee(Base, AsyncAttrs):
    __tablename__ = 'employee'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String)

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f'{DEFAULT_SCHEMA}.user.id')
    )

    # Связь с User
    # Однонаправленная связь employee → user.
    user: Mapped[List[User]] = relationship(
        'User',
        back_populates='employee',
        cascade='all, delete-orphan',  # удален сотрудник-удален пользователь
        single_parent=True,  # у сотрудника может быть только один пользователь
    )

    # Связь с Vacation
    # у сотрудника может быть несколько отпусков.
    vacations: Mapped[List[Vacation]] = relationship(
        'Vacation', back_populates='employee', cascade='all, delete-orphan'
    )
