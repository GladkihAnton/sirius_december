from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.integrations.metrics.metrics import async_integrations_timer
from webapp.models.sirius.review import Review


@async_integrations_timer
async def get_review_model(session: AsyncSession, model_id: int) -> Review | None:
    return (await session.scalars(select(Review).filter_by(id=model_id))).one_or_none()
