from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.integrations.metrics.metrics import async_integrations_timer
from webapp.models.sirius.user import User


@async_integrations_timer
async def get_user_model(session: AsyncSession, model_id: int) -> User | None:
    return (await session.scalars(select(User).filter_by(id=model_id))).one_or_none()
