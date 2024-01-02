from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.activity.utils.get_activity import get_activity_model
from webapp.api.crud.router import crud_router
from webapp.crud.activity import activity_crud
from webapp.integrations.postgres import get_session
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth
from webapp.utils.crud.serializers import serialize_model


@crud_router.get('/activity')
async def get_activity(
    review_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if review_id is None:
        serialized_activity = serialize_model(list(await activity_crud.get_all(session)))
        return ORJSONResponse({'activity': serialized_activity})

    activity = await get_activity_model(session, review_id)
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_activity = serialize_model(activity)
    return ORJSONResponse({'activity': serialized_activity})
