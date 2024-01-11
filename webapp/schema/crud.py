from pydantic import BaseModel, Field


class IdField(BaseModel):
    id: int = Field(description="Уникальный идентификатор объекта")


class CrudGetAll(BaseModel):
    limit: int = Field(
        default=10,
        description="Максимальное количество элементов в выдаче",
        examples=[1, 10],
        ge=0,
    )
    offset: int = Field(default=0, description="Сдвиг по элементам", examples=[10, 20, 30], ge=0)
