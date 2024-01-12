from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import exists
from werkzeug.security import check_password_hash, generate_password_hash

from webapp.models.tms.user import User
from webapp.schema.auth.login.user import UserLogin
from webapp.schema.auth.register.user import UserRegister


async def auth_get_user(session: AsyncSession, user_info: UserLogin) -> User | None:
    user = (
        await session.scalars(
            select(User).where(
                User.username == user_info.username,
            )
        )
    ).one_or_none()

    if user and check_password_hash(user.hashed_password, user_info.password):
        return user

    return None


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return (await session.scalars(select(User).where(User.id == user_id))).one_or_none()


async def check_user(session: AsyncSession, username: str) -> bool:
    query = select(exists().where(User.username == username))
    return bool(await session.scalar(query))


async def create_user(session: AsyncSession, user_info: UserRegister) -> None:
    user = User(
        username=user_info.username,
        hashed_password=generate_password_hash(user_info.password),
    )

    session.add(user)
    await session.commit()
