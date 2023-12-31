from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.crud.utils.operations import AsyncCRUDFactory
from webapp.models.sirius.user import User
from webapp.schema.info.user import UserInfo
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


""" # noqa Q001
async def create_user(session: AsyncSession, user_info: UserInfo) -> User:
    password = hash_password(user_info.password)
    new_user = User(username=user_info.username, password=password)

    async with session.begin():
        session.add(new_user)
        await session.flush()
    return new_user


async def get_users(session: AsyncSession) -> Sequence[User]:
    return (await session.scalars(select(User))).all()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def update_user(session: AsyncSession, user_id: int, new_user_info: UserInfo) -> User | None:
    user = await get_user_by_id(session, user_id)

    if user:
        user.username = new_user_info.username
        user.password = hash_password(new_user_info.password)
        await session.commit()

        return user
    return None


async def delete_user(session: AsyncSession, user_id: int) -> bool:
    user = await get_user_by_id(session, user_id)

    if user:
        await session.delete(user)
        await session.commit()

        return True
    return False
"""
user_crud = AsyncCRUDFactory(User)
