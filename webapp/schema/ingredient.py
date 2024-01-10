from pydantic import BaseModel
from typing import List


INGREDIENT_TABLE = 'ingredient'

class IngredientData(BaseModel):
    title: str


class IngredientResponse(BaseModel):
    id: int
    title: str


class IngredientsResponse(BaseModel):
    ingredients: List[IngredientResponse]
