from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.metrics import async_timer
from webapp.models.sirius.activity import Activity


@async_timer
async def get_activity_model(session: AsyncSession, model_id: int) -> Activity | None:
    return (await session.scalars(select(Activity).filter_by(id=model_id))).one_or_none()
