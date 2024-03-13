from enum import Enum

from sqlalchemy import Integer, String, BigInteger
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from webapp.models.meta import Base

class UserRoleEnum(Enum):
    admin = 'admin'
    customer = 'customer'
    delivery = 'delivery'


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    username: Mapped[int] = mapped_column(BigInteger, unique=True)
    code: Mapped[str] = mapped_column(String)

    role: Mapped[UserRoleEnum] = mapped_column(ENUM(UserRoleEnum, inherit_schema=True))
