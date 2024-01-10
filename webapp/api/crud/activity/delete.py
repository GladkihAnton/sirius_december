from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.activity.router import activity_router
from webapp.crud.activity import activity_crud
from webapp.integrations.cache.cache import redis_drop_key
from webapp.integrations.postgres import get_session
from webapp.models.sirius.activity import Activity
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@activity_router.post('/delete/{activity_id}')
async def delete_activity(
    activity_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> Response:
    if not await activity_crud.delete(session, activity_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await redis_drop_key(Activity.__name__, activity_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
