from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.metrics import async_integrations_timer
from webapp.models.sirius.exchange import Exchange


@async_integrations_timer
async def get_exchange(session: AsyncSession, exchange_id: int) -> Exchange | None:
    query = Exchange.id == exchange_id
    return (await session.scalars(select(Exchange).where(query))).one_or_none()
