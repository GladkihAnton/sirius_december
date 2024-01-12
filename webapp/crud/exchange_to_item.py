from sqlalchemy import Table, insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from webapp.models.sirius.item import Item
from webapp.models.sirius.exchange import Exchange
from webapp.models.sirius.exchange_to_item import exchange_to_item


async def create_relationship(session: AsyncSession, data: Any) -> int:
    data_dict = data.dict()

    await session.execute(
        insert(exchange_to_item)
        .values(**data_dict)
    )

    await session.commit()
