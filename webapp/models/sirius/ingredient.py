from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from webapp.models.meta import DEFAULT_SCHEMA, Base
from webapp.models.sirius.ingredient_to_recipe import ingredient_to_recipe


class Ingredient(Base):
    __tablename__ = 'ingredient'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String, unique=True)

    recipes: Mapped[List["Recipe"]] = relationship(secondary=ingredient_to_recipe, back_populates='ingredients')
