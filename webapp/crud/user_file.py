from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from webapp.models.sirius.user import User


async def get_user_files(session: AsyncSession, user_id: int):
    return (
        await session.scalars(
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.files),
            )
        )
    ).one_or_none()