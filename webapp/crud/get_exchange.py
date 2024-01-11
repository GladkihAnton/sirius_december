from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.sirius.exchange import Exchange
from webapp.schema.exchange import ExchangeData


async def get_exchange(session: AsyncSession, exchange_data: ExchangeData) -> Exchange | None:
    return (
        await session.scalars(
            select(Exchange).where(
                Exchange.title == exchange_data.title
            )
        )
    ).one_or_none()
