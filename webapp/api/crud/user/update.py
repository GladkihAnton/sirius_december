from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.user.router import user_router
from webapp.crud.user import user_crud
from webapp.integrations.cache.cache import redis_drop_key
from webapp.integrations.postgres import get_session
from webapp.models.sirius.user import User
from webapp.schema.info.user import UserInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@user_router.post('/update/{user_id}')
async def update_user(
    body: UserInfo,
    user_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    exists = user_crud.get_model(session, user_id) is not None

    await user_crud.update(session, user_id, body)

    await redis_drop_key(User.__name__, user_id)

    if exists:
        return ORJSONResponse(content={'message': 'User updated successfully'}, status_code=status.HTTP_204_NO_CONTENT)

    return ORJSONResponse(content={'message': 'User created successfully'}, status_code=status.HTTP_201_CREATED)
