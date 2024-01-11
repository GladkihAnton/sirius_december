from webapp.api.service.router import service_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from starlette import status
from fastapi.responses import ORJSONResponse
from webapp.pydantic_schemas.service import ServiceModel
from webapp.crud.service import update_service
from webapp.db.redis import get_redis


@service_router.put('/')
async def update_service_data(body: ServiceModel, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    redis = get_redis()
    try:
        updated_data = await update_service(body.id, body.name, body.duration, session)
        await redis.delete(f'service {id}')
        return ORJSONResponse(
            {
                'name': updated_data.name,
                'duration': updated_data.duration,
            },
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='name is already used',
        )
