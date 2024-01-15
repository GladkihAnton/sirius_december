from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.auth.router import auth_router
from webapp.crud.crud import create
from webapp.db.postgres import get_session
from webapp.models.sirius.user import User
from webapp.schema.user import UserLogin, UserLoginResponse
from webapp.utils.auth.password import hash_password


@auth_router.post(
    '/register',
    response_model=UserLoginResponse,
)
async def register(body: UserLogin, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:

    body.password = hash_password(body.password)
    user = await create(session, body, User)

    return ORJSONResponse({'id': user.id, 'username': user.username})
