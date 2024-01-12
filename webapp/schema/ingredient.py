from pydantic import BaseModel
from typing import List



class IngredientData(BaseModel):
    title: str


class IngredientResponse(BaseModel):
    id: int
    title: str


class IngredientsResponse(BaseModel):
    ingredients: List[IngredientResponse]
