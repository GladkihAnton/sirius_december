from webapp.doctor_api.router import doctor_router
from webapp.models.clinic.doctor import Doctor
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from sqlalchemy import delete
from webapp.metrics import resp_counter, errors_counter
from fastapi import Depends, HTTPException
from starlette import status
from fastapi.responses import Response
from webapp.db.redis import get_redis


@doctor_router.delete('/{id:int}')
async def delete_doctor(id: int, session: AsyncSession = Depends(get_session)) -> Response:
    resp_counter.labels(endpoint='DELETE /doctor/').inc()
    redis = get_redis()
    try:
        await session.execute(
            delete(Doctor).where(Doctor.id == id),
        )
        await session.commit()
        await redis.delete(f'doctor {id}')
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        errors_counter.labels(endpoint='DELETE /doctor/').inc()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
