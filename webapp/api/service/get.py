from webapp.api.service.router import service_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from typing import List, Any
from fastapi.responses import ORJSONResponse
from webapp.pydantic_schemas.service import ServiceModel
from webapp.crud.service import get_services, get_service
from fastapi import Depends, HTTPException
from starlette import status
from webapp.db.redis import get_redis
import orjson


@service_router.get('/page/{page_num}', response_model=List[ServiceModel])
async def get_services(page_num: int, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    services = await get_services(page_num, session)
    services_json = [ServiceModel.model_validate(service).model_dump(mode='json') for service in services]
    return ORJSONResponse(services_json)


@service_router.get('/{id:int}', response_model=ServiceModel)
async def get_service(id: int, session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    redis = get_redis()
    service_bytes = await redis.get(f'service {id}')
    if service_bytes:
        service = orjson.loads(service_bytes)
        return ORJSONResponse(service)
    try:
        service_sqlalch = await get_service(id, session)
        service = ServiceModel.model_validate(service_sqlalch).model_dump(mode='json')
        await redis.set(f'service {id}', orjson.dumps(service))
        return service
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
