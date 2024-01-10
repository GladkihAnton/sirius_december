from typing import List
from pydantic import BaseModel

class ClientInfo(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    company_name: str
    deals: List[int]
