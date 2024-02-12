from decimal import Decimal
from typing import List



from sqlalchemy import BigInteger, String, Text, DECIMAL
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from webapp.models.meta import Base


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)

    offer: Mapped[str] = mapped_column(String)

    title: Mapped[str] = mapped_column(String)

    picture_url: Mapped[str] = mapped_column(Text)

    url: Mapped[str] = mapped_column(Text)

    price: Mapped[Decimal] = mapped_column(DECIMAL)


    @hybrid_property
    def get_columns(self) -> List[str]:
        return self.__table__.columns.keys()
