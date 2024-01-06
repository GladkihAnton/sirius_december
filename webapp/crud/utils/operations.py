from typing import Any, Sequence, Type, TypeVar

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeMeta

from webapp.integrations.metrics.metrics import async_integrations_timer

ModelT = TypeVar('ModelT', bound=DeclarativeMeta)


class AsyncCRUDFactory:
    def __init__(self, model: Type[ModelT]) -> None:
        self.model = model

    @async_integrations_timer
    async def create(self, session: AsyncSession, model_info: Any) -> ModelT:
        async with session.begin_nested():
            async with session.begin_nested():
                model_info_dict = model_info.dict()

                instance = self.model(**model_info_dict)
                session.add(instance)
                await session.flush()
                await session.commit()
            return instance

    @async_integrations_timer
    async def get_all(self, session: AsyncSession) -> Sequence[ModelT]:
        return (await session.scalars(select(self.model))).all()

    @async_integrations_timer
    async def update(self, session: AsyncSession, model_id: int, model_info: Any) -> ModelT | None:
        model = self.model
        model_id_attr = getattr(model, 'id', None)

        model_info_dict = model_info.dict()

        if model_id_attr is None:
            return None
        query = update(model).where(model_id_attr == model_id).values(**model_info_dict)
        await session.execute(query)
        await session.commit()

        updated_instance = await session.get(self.model, model_id)
        return updated_instance

    @async_integrations_timer
    async def delete(self, session: AsyncSession, model_id: int) -> bool:
        instance = await session.get(self.model, model_id)
        if instance:
            await session.delete(instance)
            await session.commit()
            return True
        return False
