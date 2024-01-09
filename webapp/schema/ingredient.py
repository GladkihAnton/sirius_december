from pydantic import BaseModel


INGREDIENT_TABLE = 'ingredient'

class IngredientData(BaseModel):
    title: str


class IngredientResponse(BaseModel):
    id: int
    title: str
