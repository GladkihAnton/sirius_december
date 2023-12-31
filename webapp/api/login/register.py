from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.login.router import auth_router
from webapp.crud.user import user_crud
from webapp.integrations.postgres import get_session
from webapp.schema.info.user import UserInfo
from webapp.utils.auth.password import hash_password


@auth_router.post('/register')
async def register(
    body: UserInfo,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    body.password = hash_password(body.password)

    try:
        await user_crud.create(session, body)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={'message': 'User created successfully'}, status_code=status.HTTP_201_CREATED)
