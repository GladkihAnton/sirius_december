from webapp.patient_api.router import patient_router
from webapp.models.clinic.timetable import Timetable
from webapp.models.clinic.service import Service
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from sqlalchemy import insert, select, func
from starlette import status
from fastapi.responses import ORJSONResponse, Response
from webapp.pydantic_schemas.timetable import TimetableCreateModel
from datetime import timedelta
from webapp.metrics import resp_counter, errors_counter


@patient_router.post('/appointment')
async def make_appointment(body: TimetableCreateModel, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    resp_counter.labels(endpoint='POST /patient/appointment').inc()
    doctor_working_hours = (
        await session.scalars(
            select(Timetable.start).where(
                Timetable.doctor_id == body.doctor_id,
                func.date(Timetable.start) == func.date(body.start)
            )
        )
    ).all()
    service_duration = (await session.scalars(select(Service.duration).where(Service.id == body.service_id))).one()
    duration = timedelta(hours=service_duration.hour, minutes=service_duration.minute)
    for working_time in doctor_working_hours:
        if not(working_time - duration > body.start or working_time + duration < body.start):
            errors_counter.labels(endpoint='POST /patient/appointment').inc()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='This working time is already taken',
            )
    try:
        new_id = (
            await session.scalars(
                insert(Timetable).values(
                    {
                        'doctor_id': body.doctor_id,
                        'user_id': body.user_id,
                        'service_id': body.service_id,
                        'start': body.start,
                        'end': body.start + duration

                    },
                ).returning(Timetable.id),
            )
        ).one()
    except Exception:
        errors_counter.labels(endpoint='POST /patient/appointment').inc()
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    await session.commit()
    return ORJSONResponse(
        content={'id': new_id},
        status_code=status.HTTP_201_CREATED,
    )
