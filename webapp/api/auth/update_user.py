from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.auth.router import auth_router
from webapp.crud.crud import update
from webapp.db.postgres import get_session
from webapp.models.sirius.user import User
from webapp.schema.user import UserLogin, UserLoginResponse


@auth_router.post(
    '/update_user/{user_id}',
    response_model=UserLoginResponse,
)
async def update_user(user_id: int, body: UserLogin, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    updated_id = await update(session, user_id, body, User)

    return ORJSONResponse({'id': updated_id, 'username': body.username, 'password': body.password})
