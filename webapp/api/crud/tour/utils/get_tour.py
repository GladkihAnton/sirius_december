from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.metrics import async_timer
from webapp.models.sirius.tour import Tour


@async_timer
async def get_tour_model(session: AsyncSession, model_id: int) -> Tour | None:
    return (await session.scalars(select(Tour).filter_by(id=model_id))).one_or_none()
