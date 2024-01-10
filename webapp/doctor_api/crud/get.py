from webapp.doctor_api.router import doctor_router
from webapp.models.clinic.doctor import Doctor
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from sqlalchemy import select
from typing import Any, List
from webapp.pydantic_schemas.doctor import DoctorModel
from fastapi.responses import ORJSONResponse
from webapp.metrics import resp_counter, errors_counter
from fastapi import Depends, HTTPException
from starlette import status
from webapp.db.redis import get_redis
import orjson


@doctor_router.get('/{id:int}', response_model=DoctorModel)
async def get_doctor(id: int, session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    resp_counter.labels(endpoint='GET /doctor/').inc()
    redis = get_redis()
    doctor_bytes = await redis.get(f'doctor {id}')
    if doctor_bytes:
        doctor = orjson.loads(doctor_bytes)
        return ORJSONResponse(doctor)
    try:
        select_resp = select(Doctor).where(Doctor.id == id)
        doctor_elem = (await session.scalars(select_resp)).one()
        doctor = DoctorModel.model_validate(doctor_elem).model_dump(mode='json')
        await redis.set(f'doctor {id}', orjson.dumps(doctor))
        return doctor
    except Exception:
        errors_counter.labels(endpoint='GET /doctor/').inc()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@doctor_router.get('/all', response_model=List[DoctorModel])
async def get_doctors(session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    resp_counter.labels(endpoint='GET /doctor/all').inc()
    doctors = (await session.execute(select(Doctor))).scalars()
    doctors_json = [Doctor.model_validate(doctor).model_dump(mode='json') for doctor in doctors]
    return ORJSONResponse(doctors_json)
