from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from webapp.api.auth.router import auth_router
from webapp.db.postgres import get_session
from webapp.pydantic_schemas.user import UserLogin, UserLoginResponse
from webapp.utils.auth.jwt import jwt_auth
from webapp.models.clinic.user import User
from sqlalchemy import select
from webapp.utils.password.get_hash import hash_password


@auth_router.post(
    '/login',
    response_model=UserLoginResponse,
)
async def login(
    body: UserLogin,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    user = (
        await session.scalars(
            select(User).where(
                User.username == body.username,
                User.hashed_password == hash_password(body.password),
            )
        )
    ).one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return ORJSONResponse(
        {
            'access_token': jwt_auth.create_token(user.id),
        }
    )