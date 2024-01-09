from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from webapp.crud.models_crud import ModelsCRUD
from webapp.models.sirius.student import Student


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


async def get_all(session: AsyncSession) -> Sequence[Student]:
    return (await session.scalars(select(Student).options(selectinload(Student.user)))).all()


student_crud = ModelsCRUD(Student)
