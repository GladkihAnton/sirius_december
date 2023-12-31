from typing import List

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.router import crud_router
from webapp.crud.activity import activity_crud
from webapp.integrations.postgres import get_session
from webapp.models.sirius.activity import Activity
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth
from webapp.utils.crud.serializers import serialize_model


@crud_router.get('/activity')
async def get_activity(
    review_id: int | None = None,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if review_id is None:
        activity: List[Activity] = list(await activity_crud.get_all(session))
        serialized_activity = serialize_model(activity)
        return ORJSONResponse({'activity': serialized_activity})

    activity = await activity_crud.get(session, review_id)  # type: ignore
    if activity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_activity = serialize_model(activity)
    return ORJSONResponse({'activity': serialized_activity})
