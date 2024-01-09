from typing import Optional

from pydantic import BaseModel, ConfigDict


class InstitutionInfo(BaseModel):
    title: str
    phone: str
    email: str
    address: str
    description: Optional[str] = None


class InstitutionRead(InstitutionInfo):
    model_config = ConfigDict(from_attributes=True)

    id: int
