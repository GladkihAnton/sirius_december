from webapp.models.clinic.doctor import Doctor
from webapp.models.clinic.service import Service
from webapp.models.clinic.doctor_to_service import DoctorToService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, select
from webapp.metrics import async_integrations_timer


@async_integrations_timer
async def assign_service(doctor_id: int, service_id: int, session: AsyncSession) -> None:
    select_resp = select(Doctor).where(Doctor.id == doctor_id).options(selectinload(Doctor.services))
    doctor = (await session.scalars(select_resp)).one()
    service = (await session.scalars(select(Service).where(Service.id == service_id))).one()
    doctor.services.append(service)
    await session.commit()


@async_integrations_timer
async def get_doctor_services(doctor_id: int, session: AsyncSession):
    select_resp = select(Doctor).where(Doctor.id == doctor_id).options(selectinload(Doctor.services))
    return (await session.scalars(select_resp)).one().services


@async_integrations_timer
async def take_service_away(doctor_id: int, service_id: int, session: AsyncSession) -> None:
    await session.execute(
        delete(DoctorToService).where(
            DoctorToService.doctor_id == doctor_id,
            DoctorToService.service_id == service_id
        )
    )
    await session.commit()


@async_integrations_timer
async def get_doctors_ids_for_service(service_id: int, session: AsyncSession) -> None:
    return await (
        await session.scalars(
            select(DoctorToService.doctor_id).where(DoctorToService.service_id == service_id)
        )
    ).all()
