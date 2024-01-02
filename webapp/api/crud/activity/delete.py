from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.activity.router import activity_router
from webapp.crud.activity import activity_crud
from webapp.integrations.postgres import get_session
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@activity_router.get('/delete/{activity_id}')
async def delete_activity(
    activity_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        await activity_crud.delete(session, activity_id)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(content={'message': 'Activity removed successfully'}, status_code=status.HTTP_204_NO_CONTENT)
