from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.sirius.user import User
from webapp.schema.user import UserLogin
from webapp.utils.auth.password import hash_password


async def get_user(session: AsyncSession, user_info: UserLogin) -> User | None:
    return (
        await session.scalars(
            select(User).where(
                User.username == user_info.username,
                User.password == hash_password(user_info.password),
            )
        )
    ).one_or_none()
