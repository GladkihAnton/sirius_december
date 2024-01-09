from webapp.patient_api.router import patient_router
from webapp.models.clinic.timetable import Timetable
from webapp.models.clinic.doctor_to_service import DoctorToService
from webapp.models.clinic.service import Service
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends
from typing import List
from sqlalchemy import select, func
from fastapi.responses import ORJSONResponse
from webapp.pydantic_schemas.timetable import GetHoursResp
from datetime import timedelta, datetime, date
from webapp.patient_api.timetable_relation.config import CLOSING_TIME, OPENNING_TIME
from webapp.metrics import resp_counter


async def hours_for_service_by_doctor(date: date, doctor_id: int, service_id: int, session: AsyncSession) -> List[str]:
    free_hours = []
    service_duration = (await session.scalars(select(Service.duration).where(Service.id == service_id))).one()
    duration = timedelta(hours=service_duration.hour, minutes=service_duration.minute)
    doctor_working_hours = (
        await session.execute(
            select(Timetable.start, Timetable.end).where(
                Timetable.doctor_id == doctor_id,
                func.date(Timetable.start) == func.date(date)
            )
        )
    ).all()
    interval_point = datetime.combine(date.today(), OPENNING_TIME)
    while interval_point.time() < CLOSING_TIME:
        interval_point_flag = True
        for start, end in doctor_working_hours:
            if not(end.time() <= interval_point.time() or ((start - duration).time() >= interval_point.time())):
                interval_point_flag = False
        if interval_point_flag:
            free_hours.append(interval_point.time().isoformat())
        interval_point += duration
    return free_hours


@patient_router.post('/free_hours')
async def get_free_hours(body: GetHoursResp, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    resp_counter.labels(endpoint='POST /patient/free_hours').inc()
    if body.doctor_id:
        free_hours = await hours_for_service_by_doctor(body.search_date, body.doctor_id, body.service_id, session)
        return ORJSONResponse({'free_time': free_hours})
    doctor_ids = (
        await session.scalars(
            select(DoctorToService.doctor_id).where(DoctorToService.service_id == body.service_id)
        )
    ).all()
    result: set = set()
    for doctor_id in doctor_ids:
        free_hours: List[str] = await hours_for_service_by_doctor(body.search_date, doctor_id, body.service_id, session)
        free_hours: set[str] = set(free_hours)
        result = result.union(free_hours)
    return ORJSONResponse({'free_time': list(free_hours)})
