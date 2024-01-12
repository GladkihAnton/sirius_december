from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from webapp.crud.const import SKIP_LIMIT
from webapp.crud.models_crud import ModelsCRUD
from webapp.metrics.metrics import INTEGRATIONS_LATENCY
from webapp.models.sirius.group import Group
from webapp.models.sirius.student import Student


@INTEGRATIONS_LATENCY.time()
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


@INTEGRATIONS_LATENCY.time()
async def get_all(session: AsyncSession, offset: int) -> Sequence[Group]:
    return (
        (
            await session.execute(
                select(Group)
                .options(joinedload(Group.students).joinedload(Student.user))
                .limit(SKIP_LIMIT)
                .offset(offset)
            )
        )
        .unique()
        .scalars()
        .all()
    )


group_crud = ModelsCRUD(Group)
