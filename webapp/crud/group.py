from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from webapp.crud.models_crud import ModelsCRUD
from webapp.models.sirius.group import Group
from webapp.models.sirius.student import Student


async def get_group_by_id(session: AsyncSession, group_id: int) -> Group | None:
    return (
        (
            await session.execute(
                select(Group)
                .where(
                    Group.id == group_id,
                )
                .options(joinedload(Group.students).joinedload(Student.user))
            )
        )
        .unique()
        .scalars()
        .one_or_none()
    )


async def get_all(session: AsyncSession) -> Sequence[Group]:
    return (
        (await session.execute(select(Group).options(joinedload(Group.students).joinedload(Student.user))))
        .unique()
        .scalars()
        .all()
    )


group_crud = ModelsCRUD(Group)
