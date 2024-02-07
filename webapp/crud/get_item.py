from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.metrics import async_integrations_timer
from webapp.models.sirius.item import Item
from webapp.schema.item import ItemData


@async_integrations_timer
async def get_item(session: AsyncSession, item_data: ItemData) -> Item | None:
    return (await session.scalars(select(Item).where(Item.name == item_data.name))).one_or_none()
