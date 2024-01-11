from webapp.api.doctor.router import doctor_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends
from fastapi.responses import ORJSONResponse
from typing import List
from webapp.pydantic_schemas.service import ServiceModel
from webapp.db.redis import get_redis
from webapp.crud.doctor_to_service import get_doctor_services
import orjson


@doctor_router.get('/services/{doctor_id:int}', response_model=List[ServiceModel])
async def get_services(doctor_id: int, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    redis = get_redis()
    services_bytes = await redis.get(f'doctor {doctor_id} services')
    if services_bytes:
        services = orjson.loads(services_bytes)
        return ORJSONResponse({'services': services})
    sqlalch_obj_services = await get_doctor_services(doctor_id, session)
    services = [service.to_dict() for service in sqlalch_obj_services]
    await redis.set(f'doctor {doctor_id} services', orjson.dumps(services))

    return ORJSONResponse({'services': services})
