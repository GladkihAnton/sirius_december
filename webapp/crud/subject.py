from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from webapp.crud.models_crud import ModelsCRUD
from webapp.models.sirius.subject import Subject
from webapp.models.sirius.teacher import Teacher


async def get_subject_by_id(session: AsyncSession, teacher_id: int) -> Subject | None:
    return (
        (
            await session.execute(
                select(Subject)
                .where(Subject.id == teacher_id)
                .options(
                    joinedload(Subject.teacher).joinedload(Teacher.user),
                )
            )
        )
        .unique()
        .scalars()
        .one_or_none()
    )


async def get_all(session: AsyncSession) -> Sequence[Subject]:
    return (
        (await session.execute(select(Subject).options(joinedload(Subject.teacher).joinedload(Teacher.user))))
        .unique()
        .scalars()
        .all()
    )


subject_crud = ModelsCRUD(Subject)
