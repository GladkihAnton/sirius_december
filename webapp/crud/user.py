from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.sirius.user import User as SQLAUser
from webapp.schema.login.user import User as PydanticUser, UserLogin
from webapp.utils.auth.password import hash_password


async def get_user(
    session: AsyncSession, user_info: UserLogin
) -> SQLAUser | None:
    return (
        await session.scalars(
            select(SQLAUser).where(
                SQLAUser.username == user_info.username,
                SQLAUser.hashed_password == hash_password(user_info.password),
            )
        )
    ).one_or_none()


async def get_user_by_id(
    session: AsyncSession, user_id: int
) -> PydanticUser | None:
    result = await session.get(SQLAUser, user_id)
    print(result)
    if result:
        return PydanticUser.model_validate(result)
    return None


async def create_user(
    session: AsyncSession, username: str, email: str, hashed_password: str
) -> SQLAUser:
    new_user = SQLAUser(
        email=email, username=username, hashed_password=hashed_password
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_email(
    session: AsyncSession, email: str
) -> SQLAUser | None:
    result = await session.scalars(
        select(SQLAUser).where(SQLAUser.email == email)
    )
    return result.one_or_none()


async def get_user_by_username(
    session: AsyncSession, username: str
) -> SQLAUser | None:
    result = await session.scalars(
        select(SQLAUser).where(SQLAUser.username == username)
    )
    return result.one_or_none()
