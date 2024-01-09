from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Type, Any
from sqlalchemy.orm import DeclarativeMeta


ModelT = TypeVar('ModelT', bound=DeclarativeMeta)


async def get_all(session: AsyncSession, table: Type[ModelT]) -> ModelT | None:
    return (await session.scalars(select(table))).all()


async def create(session: AsyncSession, data: Any, model: ModelT) -> ModelT | None:
    async with session.begin_nested():
        async with session.begin_nested():
            data_dict = data.dict()
            instance = model(**data_dict)
            session.add(instance)
            await session.flush()
            await session.commit()
        return instance.id


async def delete(session: AsyncSession, id: int, table: str) -> None:
    await session.execute(delete(table).where(table.c.id == id))
    await session.commit()


async def update(session: AsyncSession, id: int, data: Any, table: str) -> None:
    await session.execute(update(table).where(table.c.id == id).values(**data))
    await session.commit()
