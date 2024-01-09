from webapp.models.meta import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Column, Table, ForeignKey
from typing import List

from webapp.models.meta import DEFAULT_SCHEMA, Base

ingredient_to_recipe = Table(
    "ingredient_to_recipe",
    Base.metadata,
    Column("ingredient_id", ForeignKey(f"{DEFAULT_SCHEMA}.ingredient.id"), primary_key=True),
    Column("recipe_id", ForeignKey(f"{DEFAULT_SCHEMA}.recipe.id"), primary_key=True),
    schema=DEFAULT_SCHEMA,
)
