from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.auth.router import auth_router
from webapp.crud.crud import delete
from webapp.db.postgres import get_session
from webapp.models.sirius.user import User
from webapp.schema.user import UserLoginResponse


@auth_router.post(
    '/delete_user/{user_id}',
    response_model=UserLoginResponse,
)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session)
    ) -> int:
    deleted_id = await delete(session, user_id, User)

    if deleted_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(
        {
            'id': deleted_id
        }
    )
