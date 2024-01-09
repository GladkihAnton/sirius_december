from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from webapp.crud.models_crud import ModelsCRUD
from webapp.models.sirius.teacher import Teacher


async def get_teacher_by_id(session: AsyncSession, teacher_id: int) -> Teacher | None:
    return (
        await session.scalars(
            select(Teacher)
            .where(Teacher.id == teacher_id)
            .options(
                selectinload(Teacher.user),
            )
        )
    ).one_or_none()


async def get_all(session: AsyncSession) -> Sequence[Teacher]:
    return (await session.scalars(select(Teacher).options(selectinload(Teacher.user)))).all()


teacher_crud = ModelsCRUD(Teacher)
