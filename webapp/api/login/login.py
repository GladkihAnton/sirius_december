from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.login.router import auth_router
from webapp.cache.rabbit.queue import declare_queue
from webapp.crud.user import get_user
from webapp.db.postgres import get_session
from webapp.schema.login.user import UserLogin, UserLoginResponse
from webapp.utils.auth.jwt import jwt_auth


@auth_router.post(
    '/login',
    response_model=UserLoginResponse,
)
async def login(
    body: UserLogin,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    user = await get_user(session, body)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    await declare_queue(user.id)

    return ORJSONResponse(
        {
            'access_token': jwt_auth.create_token(user),
            'role': user.role.value,
        }
    )
