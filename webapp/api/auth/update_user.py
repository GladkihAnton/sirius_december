from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.auth.router import auth_router
from webapp.crud.crud import update
from webapp.db.postgres import get_session
from webapp.schema.user import UserLogin, UserLoginResponse, USER_TABLE
from webapp.models.sirius.user import User


@auth_router.post(
    '/update_user/{user_id}',
    response_model=UserLoginResponse,
)
async def update_user(
    user_id: int,
    body: UserLogin,
    session: AsyncSession = Depends(get_session)
    ) -> ORJSONResponse:
    updated_id = await update(session, user_id, body, User)

    return ORJSONResponse(
        {
            'id': updated_id,
            'username': body.username,
            'password': body.password
        }
    )
