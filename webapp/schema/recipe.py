from pydantic import BaseModel
from typing import List

RECIPE_TABLE = 'recipe'

class RecipeData(BaseModel):
    title: str
    ingredients: List


class RecipeResponse(BaseModel):
    id: int
    title: str
    ingredients: List
