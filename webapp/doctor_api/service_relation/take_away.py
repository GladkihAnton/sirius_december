from webapp.models.clinic.doctor_to_service import DoctorToService
from webapp.doctor_api.router import doctor_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException, Response
from starlette import status
from sqlalchemy import delete
from webapp.pydantic_schemas.doctor import DoctorServiceID
from webapp.metrics import resp_counter, errors_counter
from webapp.db.redis import get_redis


@doctor_router.post('/service_take_away/')
async def assign_service_to_doctor(body: DoctorServiceID, session: AsyncSession = Depends(get_session)) -> Response:
    resp_counter.labels(endpoint='POST /doctor/service_take_away/').inc()
    redis = get_redis()
    try:
        await session.execute(
            delete(DoctorToService).where(
                DoctorToService.doctor_id == body.doctor_id,
                DoctorToService.service_id == body.service_id
            )
        )
        await session.commit()
        await redis.delete(f'doctor {body.doctor_id} services')
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        errors_counter.labels(endpoint='POST /doctor/service_take_away').inc()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
