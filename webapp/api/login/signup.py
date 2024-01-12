from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.login.router import auth_router
from webapp.crud.user import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from webapp.db.postgres import get_session
from webapp.schema.login.user import UserLoginResponse
from webapp.schema.registration.reg import UserRegistration
from webapp.utils.auth.jwt import jwt_auth
from webapp.utils.auth.password import hash_password


@auth_router.post(
    '/signup',
    response_model=UserLoginResponse,
    tags=['Login'],
)
async def signup(
    body: UserRegistration,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    existing_user = await get_user_by_email(session, body.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email уже используется',
        )

    existing_user = await get_user_by_username(session, body.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username уже используется',
        )

    hashed_password = hash_password(body.password)

    user = await create_user(
        session, body.username, body.email, hashed_password
    )

    return ORJSONResponse(
        {
            'access_token': jwt_auth.create_token(user.id),
        },
        status_code=status.HTTP_201_CREATED,
    )
