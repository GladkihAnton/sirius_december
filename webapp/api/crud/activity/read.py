from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.activity.router import activity_router
from webapp.crud.activity import activity_crud
from webapp.integrations.cache.cache import redis_get, redis_set
from webapp.integrations.postgres import get_session
from webapp.models.sirius.activity import Activity
from webapp.schema.info.activity import ActivityInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@activity_router.get('/page/{page}')
async def get_activities(
    page: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    serialized_activity = [
        ActivityInfo.model_validate(activity).model_dump() for activity in await activity_crud.get_page(session, page)
    ]
    return ORJSONResponse({'activity': serialized_activity})


@activity_router.get('/{activity_id}')
async def get_cached_activity(
    activity_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if cached := (await redis_get(Activity.__name__, activity_id)):
        return ORJSONResponse({'activity': cached})

    activity = await activity_crud.get_model(session, activity_id)

    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_activity = ActivityInfo.model_validate(activity).model_dump(mode='json')
    await redis_set(Activity.__name__, activity_id, serialized_activity)

    return ORJSONResponse({'activity': serialized_activity})
