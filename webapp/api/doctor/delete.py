from webapp.api.doctor.router import doctor_router
from sqlalchemy.ext.asyncio import AsyncSession
from webapp.db.postgres import get_session
from fastapi import Depends, HTTPException
from starlette import status
from fastapi.responses import Response
from webapp.db.redis import get_redis
from webapp.crud.doctor import delete_doctor


@doctor_router.delete('/{id:int}')
async def delete_doctor(id: int, session: AsyncSession = Depends(get_session)) -> Response:
    redis = get_redis()
    try:
        await delete_doctor(id, session)
        await redis.delete(f'doctor {id}')
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
