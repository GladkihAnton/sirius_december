from typing import List

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.router import crud_router
from webapp.crud.user import user_crud
from webapp.integrations.postgres import get_session
from webapp.models.sirius.user import User
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth
from webapp.utils.crud.serializers import serialize_model


@crud_router.get('/user')
async def get_user(
    user_id: int | None = None,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if user_id is None:
        users: List[User] = list(await user_crud.get_all(session))
        serialized_users = serialize_model(users)
        return ORJSONResponse({'users': serialized_users})

    user = await user_crud.get(session, user_id)  # type: ignore
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_user = serialize_model(user)
    return ORJSONResponse({'user': serialized_user})
