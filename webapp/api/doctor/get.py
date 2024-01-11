from webapp.api.doctor.router import doctor_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from typing import Any, List
from webapp.pydantic_schemas.doctor import DoctorModel
from fastapi.responses import ORJSONResponse
from fastapi import Depends, HTTPException
from webapp.crud.doctor import get_doctor, get_doctors
from starlette import status
from webapp.db.redis import get_redis
import orjson


@doctor_router.get('/{id:int}', response_model=DoctorModel)
async def get_doctor(id: int, session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    redis = get_redis()
    doctor_bytes = await redis.get(f'doctor {id}')
    if doctor_bytes:
        doctor = orjson.loads(doctor_bytes)
        return ORJSONResponse(doctor)
    try:
        doctor = await get_doctor(id, session)
        doctor_json = DoctorModel.model_validate(doctor).model_dump(mode='json')
        await redis.set(f'doctor {id}', orjson.dumps(doctor_json))
        return doctor_json
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@doctor_router.get('/page/{page_num}', response_model=List[DoctorModel])
async def get_doctors(page_num: int, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    doctors = get_doctors(page_num, session)
    doctors_json = [DoctorModel.model_validate(doctor).model_dump(mode='json') for doctor in doctors]
    return ORJSONResponse(doctors_json)
