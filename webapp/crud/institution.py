from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.crud.const import SKIP_LIMIT
from webapp.crud.models_crud import ModelsCRUD
from webapp.metrics.metrics import INTEGRATIONS_LATENCY
from webapp.models.sirius.institution import Institution


@INTEGRATIONS_LATENCY.time()
async def get_institution_by_id(session: AsyncSession, institution_id: int) -> Institution | None:
    return (
        await session.execute(
            select(Institution).where(
                Institution.id == institution_id,
            )
        )
    ).scalar_one_or_none()


@INTEGRATIONS_LATENCY.time()
async def get_all(session: AsyncSession, offset: int) -> Sequence[Institution]:
    query = (select(Institution)).limit(SKIP_LIMIT).offset(offset)
    return await session.scalars(query).all()


institution_crud = ModelsCRUD(Institution)
