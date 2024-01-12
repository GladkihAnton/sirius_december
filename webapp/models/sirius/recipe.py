from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from webapp.models.meta import DEFAULT_SCHEMA, Base


class Recipe(Base):
    __tablename__ = 'recipe'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String, unique=True)

