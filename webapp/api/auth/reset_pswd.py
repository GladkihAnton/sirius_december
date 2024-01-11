from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from webapp.api.auth.router import auth_router
from webapp.db.postgres import get_session
from webapp.pydantic_schemas.user import UserChangePassword
from webapp.utils.auth.jwt import jwt_auth
from webapp.models.clinic.user import User
from sqlalchemy import select
from webapp.utils.password.get_hash import hash_password
from webapp.utils.auth.jwt import JwtTokenT


@auth_router.post('/password')
async def reset_password(
    body: UserChangePassword,
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
    session: AsyncSession = Depends(get_session)
):
    user = (
        await session.scalars(
            select(User).where(User.id == access_token['user_id']))
    ).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )
    if user.hashed_password == hash_password(body.password):
        user.hashed_password = hash_password(body.new_password)
        await session.commit()
        return Response(status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='invalid password',
        )
