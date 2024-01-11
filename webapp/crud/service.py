from webapp.models.clinic.service import Service
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, insert, update
from webapp.metrics import async_integrations_timer
from webapp.api.doctor.config import PAGE_LIMIT
from datetime import time


@async_integrations_timer
async def get_service_duration(service_id: int, session: AsyncSession):
    return (await session.scalars(select(Service.duration).where(Service.id == service_id))).one()


@async_integrations_timer
async def delete_service(service_id: int, session: AsyncSession) -> None:
    await session.execute(
        delete(Service).where(Service.id == service_id),
    )
    await session.commit()


@async_integrations_timer
async def get_services(page_num: int, session: AsyncSession):
    return (await session.execute(
        select(Service).limit(PAGE_LIMIT).offset(page_num)
    )).scalars()


@async_integrations_timer
async def get_service(id: int, session: AsyncSession):
    select_resp = select(Service).where(Service.id == id)
    return (await session.scalars(select_resp)).one()


@async_integrations_timer
async def create_service(name: str, duration: time, session: AsyncSession):
    return (
        await session.scalars(
            insert(Service).values(
                {
                    'name': name,
                    'duration': duration,
                },
            ).returning(Service.id),
        )
    ).one()


@async_integrations_timer
async def update_service(id: int, name: str, duration: time, session: AsyncSession):
    updated_data = (
        await session.execute(
            update(Service)
            .where(Service.id == id)
            .values({
                    'name': name,
                    'duration': duration,
                    }).returning(Service.name, Service.duration)
        )
    ).one()
    await session.commit()
    return updated_data
