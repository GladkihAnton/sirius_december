from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.activity.router import activity_router
from webapp.crud.activity import activity_crud
from webapp.integrations.cache.cache import redis_drop_key
from webapp.integrations.postgres import get_session
from webapp.models.sirius.activity import Activity
from webapp.schema.info.activity import ActivityInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@activity_router.post('/update/{activity_id}')
async def update_activity(
    body: ActivityInfo,
    activity_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    exists = activity_crud.get_model(session, activity_id) is not None

    await activity_crud.update(session, activity_id, body)

    await redis_drop_key(Activity.__name__, activity_id)

    if exists:
        return ORJSONResponse(
            content={'message': 'Activity updated successfully'}, status_code=status.HTTP_204_NO_CONTENT
        )

    return ORJSONResponse(content={'message': 'Activity created successfully'}, status_code=status.HTTP_201_CREATED)
