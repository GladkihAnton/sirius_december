from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.sirius.reservation import Reservation


async def get_reservation_model(session: AsyncSession, model_id: int) -> Reservation | None:
    return (await session.scalars(select(Reservation).filter_by(id=model_id))).one_or_none()
