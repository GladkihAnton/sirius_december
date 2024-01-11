from webapp.api.service.router import service_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from webapp.crud.service import create_service
from starlette import status
from fastapi.responses import ORJSONResponse
from webapp.pydantic_schemas.service import ServiceCreateModel


@service_router.post('/')
async def create_service(body: ServiceCreateModel, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    try:
        new_id = await create_service(body.name, body.duration, session)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='name is already used',
        )
    await session.commit()
    return ORJSONResponse(
        content={'id': new_id},
        status_code=status.HTTP_201_CREATED,
    )
