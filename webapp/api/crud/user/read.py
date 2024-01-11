from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.user.router import user_router
from webapp.crud.user import user_crud
from webapp.db.postgres import get_session
from webapp.integrations.cache.cache import redis_get, redis_set
from webapp.models.sirius.user import User
from webapp.schema.info.user import UserInfo, UserListResponse, UserResponse
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@user_router.get('/page/{page}', response_model=UserListResponse)
async def users_get(
    page: int,
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    serialized_users = [UserInfo.model_validate(user).model_dump() for user in await user_crud.get_page(session, page)]
    return ORJSONResponse({'users': serialized_users}, status_code=status.HTTP_200_OK)


@user_router.get('/{user_id}', response_model=UserResponse)
async def get_cached_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if cached := (await redis_get(User.__name__, user_id)):
        return ORJSONResponse({'cached_user': cached})

    user = await user_crud.get_model(session, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    serialized_order = UserInfo(**user.__dict__).model_dump(mode='json')
    await redis_set(User.__name__, user_id, serialized_order)

    return ORJSONResponse({'user': serialized_order}, status_code=status.HTTP_200_OK)
