from pydantic import BaseModel
from typing import List


class RecipeData(BaseModel):
    title: str
    ingredients: List[str]


class RecipeTitle(BaseModel):
    title: str


class RecipeIngredients(BaseModel):
    ingredients: List[str]


class RecipeIngredient(BaseModel):
    ingredient: str


class RecipeId(BaseModel):
    id: int


class RecipeResponse(BaseModel):
    id: int
    title: str
    ingredients: List[str]


class RecipesResponse(BaseModel):
    recipes: List[RecipeResponse]
