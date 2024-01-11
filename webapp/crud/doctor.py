from webapp.models.clinic.doctor import Doctor
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, insert, update
from webapp.metrics import async_integrations_timer
from webapp.api.doctor.config import PAGE_LIMIT


@async_integrations_timer
async def delete_doctor(doctor_id: int, session: AsyncSession) -> None:
    await session.execute(
        delete(Doctor).where(Doctor.id == doctor_id),
    )
    await session.commit()


@async_integrations_timer
async def get_doctor(doctor_id: int, session: AsyncSession):
    return (await session.scalars(
        select(Doctor).where(Doctor.id == doctor_id)
    )
    ).one()


@async_integrations_timer
async def get_doctors(page_num: int, session: AsyncSession):
    return (
        await session.execute(
            select(Doctor).limit(PAGE_LIMIT).offset(page_num)
        )
    ).scalars()


@async_integrations_timer
async def create_doctor(last_name: str, first_name: str, specialization: str, session: AsyncSession):
    return (
        await session.scalars(
            insert(Doctor).values(
                {
                    'last_name': last_name,
                    'first_name': first_name,
                    'specialization': specialization,
                },
            ).returning(Doctor.id),
        )
    ).one()


@async_integrations_timer
async def update_doctor(doctor_id: int, last_name: str, first_name: str, specialization: str, session: AsyncSession):
    updated_data = (
        await session.execute(
            update(Doctor)
            .where(Doctor.id == doctor_id)
            .values({
                'last_name': last_name,
                'first_name': first_name,
                'specialization': specialization,
            }).returning(Doctor.last_name, Doctor.first_name, Doctor.specialization)
        )
    ).one()
    await session.commit()
    return updated_data
