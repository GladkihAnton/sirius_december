from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.auth.router import auth_router
from webapp.crud.crud import create
from webapp.db.postgres import get_session
from webapp.schema.user import UserLogin, UserLoginResponse, USER_TABLE
from webapp.models.sirius.user import User


@auth_router.post(
    '/register',
    response_model=UserLoginResponse,
)
async def register(body: UserLogin, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    user_id = await create(session, body, User)

    return ORJSONResponse(
        {
            'id': user_id,
            'username': body.username
        }
    )
