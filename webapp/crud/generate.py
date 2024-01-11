from typing import Any, Sequence, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta, InstrumentedAttribute

from webapp.metrics import async_integrations_timer
from webapp.models.exceptions import ItemNotFound
from webapp.models.meta import Base

ModelT = TypeVar("ModelT", bound=DeclarativeMeta)


@async_integrations_timer
async def create_item(session: AsyncSession, model: type[ModelT], item: Any) -> ModelT:
    db_item = model(**item.dict())
    session.add(db_item)
    await session.commit()
    return db_item


@async_integrations_timer
async def get_items(session: AsyncSession, model: type[Base], skip: int = 0, limit: int = 10) -> Sequence[ModelT]:
    query = await session.scalars(select(model).offset(skip).limit(limit))
    return query.all()


@async_integrations_timer
async def get_item(session: AsyncSession, model: type[Base], item_id: int) -> ModelT:
    db_item = await session.get(model, item_id)
    if db_item is None:
        raise ItemNotFound()
    return db_item


@async_integrations_timer
async def update_item(session: AsyncSession, model: type[ModelT], item_id: int, item: Any) -> ModelT:
    db_item = await session.get(model, item_id)
    if db_item is None:
        raise ItemNotFound()
    for key, value in item.dict().items():
        if isinstance(getattr(model, key), InstrumentedAttribute):
            setattr(db_item, key, value)
    await session.commit()
    return db_item


@async_integrations_timer
async def delete_item(session: AsyncSession, model: type[ModelT], item_id: int) -> dict[str, str]:
    db_item = await session.get(model, item_id)
    if db_item is None:
        raise ItemNotFound()
    await session.delete(db_item)
    await session.commit()
    return {"message": "Item deleted"}
