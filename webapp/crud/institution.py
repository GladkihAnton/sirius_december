from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.crud.models_crud import ModelsCRUD
from webapp.models.sirius.institution import Institution


async def get_institution_by_id(session: AsyncSession, institution_id: int) -> Institution | None:
    return (
        await session.execute(
            select(Institution).where(
                Institution.id == institution_id,
            )
        )
    ).scalar_one_or_none()


async def get_all(session: AsyncSession) -> Sequence[Institution]:
    return (await session.scalars(select(Institution))).all()


institution_crud = ModelsCRUD(Institution)
