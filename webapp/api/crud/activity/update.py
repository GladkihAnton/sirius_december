from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.activity.router import activity_router
from webapp.crud.activity import activity_crud
from webapp.integrations.postgres import get_session
from webapp.schema.info.activity import ActivityInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@activity_router.post('/update/{activity_id}')
async def get_activity(
    body: ActivityInfo,
    activity_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if await activity_crud.update(session, activity_id, body) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(content={'message': 'Activity updated successfully'}, status_code=status.HTTP_204_NO_CONTENT)
