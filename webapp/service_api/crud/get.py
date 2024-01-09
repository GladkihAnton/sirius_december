from webapp.service_api.router import service_router
from webapp.models.clinic.service import Service
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from sqlalchemy import select
from typing import List, Any
from fastapi.responses import ORJSONResponse
from webapp.pydantic_schemas.service import ServiceModel
from webapp.metrics import resp_counter, errors_counter
from fastapi import Depends, HTTPException
from starlette import status
from webapp.db.redis import get_redis
import json
import ast


@service_router.get('/all', response_model=List[ServiceModel])
async def get_services(session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    resp_counter.labels(endpoint='GET /service/all').inc()
    services = (await session.execute(select(Service))).scalars()
    services_json = [ServiceModel.model_validate(service).model_dump(mode='json') for service in services]
    return ORJSONResponse(services_json)


@service_router.get('/{id:int}', response_model=ServiceModel)
async def get_service(id: int, session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    resp_counter.labels(endpoint='GET /service/').inc()
    redis = get_redis()
    service_bytes = await redis.get(f'doctor {id}')
    if service_bytes:
        service = ast.literal_eval(service_bytes.decode('utf-8'))
        return ORJSONResponse(service)
    try:
        select_resp = select(Service).where(Service.id == id)
        service_sqlalch = (await session.scalars(select_resp)).one()
        service = ServiceModel.model_validate(service_sqlalch).model_dump(mode='json')
        await redis.set(f'doctor {id}', json.dumps(service))
        return service
    except Exception:
        errors_counter.labels(endpoint='GET /service/').inc()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
