from webapp.api.service.router import service_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from starlette import status
from fastapi.responses import Response
from webapp.crud.service import delete_service
from webapp.db.redis import get_redis


@service_router.delete('/{id:int}')
async def delete_service(id: int, session: AsyncSession = Depends(get_session)) -> Response:
    redis = get_redis()
    try:
        delete_service(id, session)
        await redis.delete(f'service {id}')
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
