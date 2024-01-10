from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

from webapp.models.meta import DEFAULT_SCHEMA, Base
# from webapp.models.sirius.ingredient import Ingredient
from webapp.models.sirius.ingredient_to_recipe import ingredient_to_recipe


class Recipe(Base):
    __tablename__ = 'recipe'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String, unique=True)

    ingredients: Mapped[List["Ingredient"]] = relationship(secondary=ingredient_to_recipe, back_populates='recipes') #, cascade="all, delete-orphan")
