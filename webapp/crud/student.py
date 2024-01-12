from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from webapp.crud.const import SKIP_LIMIT
from webapp.crud.models_crud import ModelsCRUD
from webapp.metrics.metrics import INTEGRATIONS_LATENCY
from webapp.models.sirius.student import Student


@INTEGRATIONS_LATENCY.time()
async def get_student_by_id(session: AsyncSession, teacher_id: int) -> Student | None:
    return (
        await session.scalars(
            select(Student)
            .where(Student.id == teacher_id)
            .options(
                selectinload(Student.user),
            )
        )
    ).one_or_none()


@INTEGRATIONS_LATENCY.time()
async def get_all(session: AsyncSession, offset: int) -> Sequence[Student]:
    return (
        await session.scalars(select(Student).options(selectinload(Student.user)).limit(SKIP_LIMIT).offset(offset))
    ).all()


student_crud = ModelsCRUD(Student)
