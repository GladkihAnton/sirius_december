from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.auth.router import auth_router
from webapp.crud.user import check_user, create_user
from webapp.db.postgres import get_session
from webapp.schema.auth.register.user import UserRegister


@auth_router.post("/register")
async def register(
    body: UserRegister,
    session: AsyncSession = Depends(get_session),
) -> Response:
    user_exists = await check_user(session, body.username)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    await create_user(session, body)

    return Response(status_code=status.HTTP_201_CREATED)
