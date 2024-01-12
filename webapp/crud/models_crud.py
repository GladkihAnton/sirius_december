from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

from webapp.metrics.metrics import INTEGRATIONS_LATENCY

ModelT = TypeVar('ModelT', bound=DeclarativeMeta)
ModelInfoT = TypeVar('ModelInfoT', bound=BaseModel)


@dataclass
class ModelsCRUD(Generic[ModelT]):
    model: Type[ModelT]

    @INTEGRATIONS_LATENCY.time()
    async def create(self, session: AsyncSession, model_info: ModelInfoT) -> int:
        async with session.begin_nested():
            query = insert(self.model).values(model_info.model_dump())
            result = await session.execute(query)
            await session.commit()
        return result.inserted_primary_key[0]

    @INTEGRATIONS_LATENCY.time()
    async def update(self, session: AsyncSession, model_info: ModelInfoT, model_id: int) -> bool:
        id_attr = getattr(self.model, 'id', None)
        if id_attr is None:
            return False

        query = update(self.model).where(id_attr == model_id).values(**model_info.model_dump())
        result = await session.execute(query)

        await session.commit()

        return result.rowcount == 1

    @INTEGRATIONS_LATENCY.time()
    async def delete(self, session: AsyncSession, model_id: int) -> bool:
        id_attr = getattr(self.model, 'id', None)
        if id_attr is None:
            return False

        query = delete(self.model).where(id_attr == model_id)
        result = await session.execute(query)

        await session.commit()

        return result.rowcount == 1
