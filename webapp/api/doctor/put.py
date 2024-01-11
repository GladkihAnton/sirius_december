from webapp.api.doctor.router import doctor_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from webapp.pydantic_schemas.doctor import DoctorModel
from fastapi.responses import ORJSONResponse
from fastapi import Depends, HTTPException
from webapp.crud.doctor import update_doctor
from starlette import status
from webapp.db.redis import get_redis


@doctor_router.put('/')
async def update_doctor(body: DoctorModel, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    redis = get_redis()
    try:
        updated_data = update_doctor(body.id, body.last_name, body.first_name, body.specialization, session)
        await redis.delete(f'doctor {body.id}')
        return ORJSONResponse(
            {
                'last_name': updated_data.last_name,
                'first_name': updated_data.first_name,
                'specialization': updated_data.specialization,
            },
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
