from pydantic import BaseModel
from typing import List



class AssociationData(BaseModel):
    ingredient_id: int
    recipe_id: int
