from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.sirius.user import User
from webapp.schema.login.user import UserLogin
from webapp.utils.auth.password import hash_password


async def get_user(session: AsyncSession, user_info: UserLogin) -> User | None:
    return (
        await session.scalars(
            select(User).where(
                User.username == user_info.username,
                User.hashed_password == hash_password(user_info.password),
            )
        )
    ).one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    result = await session.scalars(select(User).where(User.id == user_id))
    return result.one_or_none()


async def create_user(session: AsyncSession, username: str, email: str, hashed_password: str) -> User:
    new_user = User(email=email, username=username, hashed_password=hashed_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.scalars(select(User).where(User.email == email))
    return result.one_or_none()


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.scalars(select(User).where(User.username == username))
    return result.one_or_none()
