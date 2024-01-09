from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    description: str