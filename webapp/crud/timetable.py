from webapp.models.clinic.timetable import Timetable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, insert, func
from webapp.metrics import async_integrations_timer
from datetime import date, datetime, timedelta


@async_integrations_timer
async def delete_timetable_point(id: int, session: AsyncSession) -> None:
    await session.execute(
        delete(Timetable).where(Timetable.id == id),
    )
    await session.commit()


@async_integrations_timer
async def timetable_point_time_for_doctor(
    doctor_id: int,
    date: date,
    session: AsyncSession
):
    return (
        await session.execute(
            select(Timetable.start, Timetable.end).where(
                Timetable.doctor_id == doctor_id,
                func.date(Timetable.start) == func.date(date)
            )
        )
    ).all()


@async_integrations_timer
async def timetable_point_start_for_doctor(doctor_id: int, start: datetime, session: AsyncSession):
    return (
        await session.scalars(
            select(Timetable.start).where(
                Timetable.doctor_id == doctor_id,
                func.date(Timetable.start) == func.date(start)
            )
        )
    ).all()


@async_integrations_timer
async def make_appointment(
        doctor_id: int,
        user_id: int,
        service_id: int,
        start: datetime,
        duration: timedelta,
        session: AsyncSession):
    return (
        await session.scalars(
            insert(Timetable).values(
                {
                    'doctor_id': doctor_id,
                    'user_id': user_id,
                    'service_id': service_id,
                    'start': start,
                    'end': start + duration

                },
            ).returning(Timetable.id),
        )
    ).one()
