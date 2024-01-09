from dataclasses import dataclass
from typing import Generic, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

ModelT = TypeVar('ModelT', bound=DeclarativeMeta)
ModelInfoT = TypeVar('ModelInfoT', bound=BaseModel)


@dataclass
class ModelsCRUD(Generic[ModelT]):
    model: Type[ModelT]

    async def create(self, session: AsyncSession, model_info: ModelInfoT) -> int:
        async with session.begin():
            query = insert(self.model).values(model_info.dict())
            result = await session.execute(query)
            await session.commit()
        return result.inserted_primary_key[0]

    async def update(self, session: AsyncSession, model_info: ModelInfoT, model_id: int) -> Optional[ModelT]:
        id_attr = getattr(self.model, 'id', None)
        if id_attr is None:
            return None

        query = update(self.model).where(id_attr == model_id).values(**model_info.dict())
        result = await session.execute(query)

        await session.commit()

        if result.rowcount == 0:
            return None

        updated_instance = await session.get(self.model, model_id)
        return updated_instance

    async def delete(self, session: AsyncSession, model_id: int) -> bool:
        id_attr = getattr(self.model, 'id', None)
        if id_attr is None:
            return False

        query = delete(self.model).where(id_attr == model_id)
        result = await session.execute(query)

        await session.commit()

        return result.rowcount == 1
