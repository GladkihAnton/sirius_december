from pydantic import BaseModel
from typing import List



class AssociationData(BaseModel):
    exchange_id: int
    item_id: int