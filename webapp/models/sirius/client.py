from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.deal import Deal

class Client(Base):
    __tablename__ = 'client'
    __table_args__ = {'schema': DEFAULT_SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.user.id'))

    first_name: Mapped[str] = mapped_column(String, unique=True)

    last_name: Mapped[str] = mapped_column(String)
    
    company_name: Mapped[str] = mapped_column(String)
    
    deals: Mapped[List['Deal']] = relationship('Deal', back_populates='client')