from sqlalchemy import Table, insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Type, Any, List
from sqlalchemy.orm import DeclarativeMeta




# async def get_all(session: AsyncSession, table: Type[ModelT]) -> List[ModelT] | None:
#     return (await session.scalars(sqlalchemy.select(table))).all()


async def create_relationship(session: AsyncSession, data: Any, table: Table) -> int:
    data_dict = data.dict()
    await session.execute(insert(table).values(**data_dict))
    await session.commit()
    # return instance.id
