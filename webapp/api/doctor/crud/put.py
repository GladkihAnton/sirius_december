from webapp.api.doctor.router import doctor_router
from webapp.models.clinic.doctor import Doctor
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from sqlalchemy import update
from webapp.pydantic_schemas.doctor import DoctorModel
from fastapi.responses import ORJSONResponse
from webapp.metrics import resp_counter, errors_counter
from fastapi import Depends, HTTPException
from starlette import status
from webapp.db.redis import get_redis


@doctor_router.put('/')
async def update_doctor(body: DoctorModel, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    resp_counter.labels(endpoint='PUT /doctor/').inc()
    redis = get_redis()
    try:
        updated_data = (
            await session.execute(
                update(Doctor)
                .where(Doctor.id == body.id)
                .values({
                    'last_name': body.last_name,
                    'first_name': body.first_name,
                    'specialization': body.specialization,
                }).returning(Doctor.last_name, Doctor.first_name, Doctor.specialization)
            )
        ).one()
        await session.commit()
        await redis.delete(f'doctor {body.id}')
        return ORJSONResponse(
            {
                'last_name': updated_data.last_name,
                'first_name': updated_data.first_name,
                'specialization': updated_data.specialization,
            },
        )
    except Exception:
        errors_counter.labels(endpoint='PUT /doctor/').inc()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
