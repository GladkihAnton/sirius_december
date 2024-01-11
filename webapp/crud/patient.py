from webapp.models.clinic.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, insert, update
from webapp.metrics import async_integrations_timer
from webapp.api.doctor.config import PAGE_LIMIT
from webapp.utils.password.get_hash import hash_password


@async_integrations_timer
async def delete_user(patient_id: int, session: AsyncSession) -> None:
    await session.execute(
        delete(User).where(User.id == patient_id),
    )
    await session.commit()


@async_integrations_timer
async def get_users(page_num: int, session: AsyncSession):
    return (await session.execute(
        select(User).limit(PAGE_LIMIT).offset(page_num)
    )
    ).scalars()


@async_integrations_timer
async def get_user(user_id: int, session: AsyncSession):
    select_resp = select(User).where(User.id == user_id)
    return (await session.scalars(select_resp)).one()


@async_integrations_timer
async def create_user(username: str, first_name: str, last_name: str, password: str, session: AsyncSession):
    return (
        await session.scalars(
            insert(User).values(
                {
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'hashed_password': hash_password(password),
                },
            ).returning(User.id),
        )
    ).one()


@async_integrations_timer
async def update_user(patient_id: int, username: str, first_name: str, last_name: str, session: AsyncSession):
    updated_data = (
        await session.execute(
            update(User)
            .where(User.id == patient_id)
            .values({
                    'username': username,
                    'last_name': last_name,
                    'first_name': first_name,
                    }).returning(User.username, User.first_name, User.last_name),
        )
    ).one()
    await session.commit()
    return updated_data
