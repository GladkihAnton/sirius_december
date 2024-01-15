from typing import List

from pydantic import BaseModel


class IngredientData(BaseModel):
    title: str


class IngredientResponse(BaseModel):
    id: int
    title: str


class IngredientsResponse(BaseModel):
    ingredients: List[IngredientResponse]
