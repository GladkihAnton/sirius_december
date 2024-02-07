from typing import List
from pydantic import BaseModel

class ClientInfo(BaseModel):
    first_name: str
    last_name: str
    company_name: str