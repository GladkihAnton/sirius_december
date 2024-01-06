from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.activity.router import activity_router
from webapp.crud.activity import activity_crud
from webapp.integrations.cache.cache import redis_get, redis_set
from webapp.integrations.postgres import get_session
from webapp.models.sirius.activity import Activity
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth
from webapp.utils.crud.serializers import serialize_model


@activity_router.get('/')
async def get_activities(
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    serialized_activity = serialize_model(list(await activity_crud.get_all(session)))
    return ORJSONResponse({'activity': serialized_activity})


@activity_router.get('/{activity_id}')
async def get_cached_activity(
    activity_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if cached := (await redis_get(Activity.__name__, activity_id)):
        return ORJSONResponse({'cached_activity': cached})

    activity = await activity_crud.get_model(session, activity_id)

    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_activity = serialize_model(activity)
    await redis_set(Activity.__name__, activity_id, serialized_activity)

    return ORJSONResponse({'activity': serialized_activity})
