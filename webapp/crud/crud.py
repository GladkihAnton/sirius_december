import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Type, Any, List
from sqlalchemy.orm import DeclarativeMeta


ModelT = TypeVar('ModelT', bound=DeclarativeMeta)


async def get_all(session: AsyncSession, table: Type[ModelT]) -> List[ModelT] | None:
    return (await session.scalars(sqlalchemy.select(table))).all()


async def create(session: AsyncSession, data: Any, model: ModelT) -> ModelT:
    # data_dict = data.dict()
    # instance = await session.execute(insert(model).values(**data_dict))
    # await session.commit()
    # return instance.id
    async with session.begin_nested():
        async with session.begin_nested():
            data_dict = data.dict()
            instance = model(**data_dict)
            session.add(instance)
            await session.flush()
            await session.commit()
        return instance


async def delete(session: AsyncSession, id: int, model: ModelT) -> int:
    deleted_id = (await session.execute(
        sqlalchemy.delete(model)
        .where(model.id == id)
        .returning(model.id)
    )).one_or_none()[0]
    await session.commit()
    return deleted_id


async def update(session: AsyncSession, id: int, data: Any, model: ModelT) -> int:
    data_dict = data.dict()
    if 'exchanges' in data_dict and not data_dict['exchanges']:
        del data_dict['exchanges']
    updated_id = (await session.execute(
        sqlalchemy.update(model)
        .where(model.id == id)
        .values(**data_dict)
        .returning(model.id)
    )).one_or_none()[0]
    await session.commit()
    return updated_id
