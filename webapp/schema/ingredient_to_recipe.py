from pydantic import BaseModel


class AssociationData(BaseModel):
    ingredient_id: int
    recipe_id: int
