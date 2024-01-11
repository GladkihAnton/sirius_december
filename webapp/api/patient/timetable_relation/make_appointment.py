from webapp.api.patient.router import patient_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from webapp.crud.timetable import timetable_point_start_for_doctor, make_appointment
from webapp.crud.service import get_service_duration
from starlette import status
from fastapi.responses import ORJSONResponse, Response
from webapp.pydantic_schemas.timetable import TimetableCreateModel
from datetime import timedelta


@patient_router.post('/appointment')
async def make_appointment(body: TimetableCreateModel, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    doctor_working_hours = timetable_point_start_for_doctor(body.doctor_id, body.start, session)
    service_duration = get_service_duration(body.service_id, session)
    duration = timedelta(hours=service_duration.hour, minutes=service_duration.minute)
    for working_time in doctor_working_hours:
        if not(working_time - duration > body.start or working_time + duration < body.start):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='This working time is already taken',
            )
    try:
        new_id = make_appointment(body.doctor_id, body.user_id, body.service_id, body.start, duration, session)
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    await session.commit()
    return ORJSONResponse(
        content={'id': new_id},
        status_code=status.HTTP_201_CREATED,
    )
