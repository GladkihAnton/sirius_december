from typing import Any, Sequence, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeMeta

from webapp.integrations.metrics.metrics import async_integrations_timer

ModelT = TypeVar('ModelT', bound=DeclarativeMeta)
PAGE_LIMIT = 10


class AsyncCRUDFactory:
    def __init__(self, model: Type[ModelT]) -> None:
        self.model = model

    @async_integrations_timer
    async def create(self, session: AsyncSession, model_info: Any) -> ModelT:
        async with session.begin_nested():
            model_info_dict = model_info.dict()

            instance = self.model(**model_info_dict)
            session.add(instance)
            await session.flush()
            await session.commit()
        return instance

    @async_integrations_timer
    async def get_page(self, session: AsyncSession, page: int) -> Sequence[ModelT]:
        return (await session.scalars(select(self.model).limit(PAGE_LIMIT).offset(page))).all()

    @async_integrations_timer
    async def get_model(self, session: AsyncSession, model_id: int) -> ModelT | None:
        return await session.get(self.model, model_id)

    @async_integrations_timer
    async def update(self, session: AsyncSession, model_id: int, model_info: Any) -> None:
        record_to_update = await session.get(self.model, model_id)

        model_info_dict = model_info.model_dump()
        for attr, value in model_info_dict.items():
            setattr(record_to_update, attr, value)

        await session.commit()

    @async_integrations_timer
    async def delete(self, session: AsyncSession, model_id: int) -> bool:
        instance = await session.get(self.model, model_id)
        if instance:
            await session.delete(instance)
            await session.commit()
            return True
        return False
