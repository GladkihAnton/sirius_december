from webapp.api.doctor.router import doctor_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException, Response
from starlette import status
from webapp.pydantic_schemas.doctor import DoctorServiceID
from webapp.crud.doctor_to_service import take_service_away
from webapp.db.redis import get_redis


@doctor_router.post('/service_take_away/')
async def take_away(body: DoctorServiceID, session: AsyncSession = Depends(get_session)) -> Response:
    redis = get_redis()
    try:
        take_service_away(body.doctor_id, body.service_id, session)
        await redis.delete(f'doctor {body.doctor_id} services')
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
