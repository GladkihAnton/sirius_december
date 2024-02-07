from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.metrics import async_integrations_timer
from webapp.models.sirius.exchange_item import ExchangeItem


@async_integrations_timer
async def get_exchange_item(session: AsyncSession, exchange_id: int = None, item_id: int = None) -> ExchangeItem | None:
    if exchange_id:
        query = ExchangeItem.exchange_id == exchange_id
    elif item_id:
        query = ExchangeItem.item_id == item_id
    return (await session.scalars(select(ExchangeItem).where(query))).one_or_none()
