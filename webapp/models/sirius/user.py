from enum import Enum
from typing import List, TYPE_CHECKING

from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import Base

if TYPE_CHECKING:
    from webapp.models.sirius.order import Order


class UserRoleEnum(Enum):
    admin = 'admin'
    customer = 'customer'
    delivery = 'delivery'


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    username: Mapped[int] = mapped_column(BigInteger, unique=True)
    tg: Mapped[str] = mapped_column(String)

    code: Mapped[str] = mapped_column(String)

    address: Mapped[str] = mapped_column(String)

    role: Mapped[UserRoleEnum] = mapped_column(ENUM(UserRoleEnum, inherit_schema=True))

    orders: Mapped[List['Order']] = relationship('Order', back_populates='user')
