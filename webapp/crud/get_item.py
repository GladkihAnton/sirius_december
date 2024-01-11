from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from webapp.models.sirius.item import Item
from webapp.schema.item import ItemData


async def get_item(session: AsyncSession, item_data: ItemData) -> Optional[Item]:
    query = select(Item).options(selectinload(Item.exchanges))
    condition = Item.title == item_data.title
    result_item = await session.execute(query.where(condition))
    return result_item.scalar_one_or_none()
