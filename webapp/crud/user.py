from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.crud.utils.operations import AsyncCRUDFactory
from webapp.integrations.metrics.metrics import async_integrations_timer
from webapp.models.sirius.user import User
from webapp.schema.info.user import UserInfo
from webapp.utils.auth.password import hash_password


@async_integrations_timer
async def get_user(session: AsyncSession, user_info: UserInfo) -> User | None:
    return (
        await session.scalars(
            select(User).where(
                User.username == user_info.username,
                User.password == hash_password(user_info.password),
            )
        )
    ).one_or_none()


user_crud = AsyncCRUDFactory(User)
