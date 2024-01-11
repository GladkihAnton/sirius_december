from webapp.api.doctor.router import doctor_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException, Response
from starlette import status
from webapp.pydantic_schemas.doctor import DoctorServiceID
from webapp.crud.doctor_to_service import assign_service
from webapp.db.redis import get_redis


@doctor_router.post('/assign_service/')
async def assign_service_to_doctor(body: DoctorServiceID, session: AsyncSession = Depends(get_session)) -> Response:
    redis = get_redis()
    try:
        assign_service(body.doctor_id, body.service_id, session)
        await redis.delete(f'doctor {body.doctor_id} services')
        return Response(status_code=status.HTTP_200_OK)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
