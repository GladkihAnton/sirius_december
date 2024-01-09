from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.crud.models_crud import ModelsCRUD
from webapp.models.sirius.user import User
from webapp.schema.user import UserInfo
from webapp.utils.auth.password import hash_password


async def get_user(session: AsyncSession, user_info: UserInfo) -> User | None:
    return (
        await session.scalars(
            select(User).where(
                User.username == user_info.username,
                User.password == hash_password(user_info.password),
            )
        )
    ).one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return (
        await session.execute(
            select(User).where(
                User.id == user_id,
            )
        )
    ).scalar_one_or_none()


user_crud = ModelsCRUD(User)
