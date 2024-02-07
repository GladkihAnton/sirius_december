from pydantic import BaseModel


class AssociationData(BaseModel):
    exchange_id: int
    item1_id: int
    item2_id: int