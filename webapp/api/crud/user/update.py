from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.user.router import user_router
from webapp.crud.user import user_crud
from webapp.integrations.postgres import get_session
from webapp.schema.info.user import UserInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@user_router.get('/user/update')
async def update_user(
    body: UserInfo,
    user_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        await user_crud.update(session, user_id, body)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(content={'message': 'User removed successfully'}, status_code=status.HTTP_204_NO_CONTENT)
