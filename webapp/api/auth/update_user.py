from fastapi import HTTPException
from fastapi.responses import ORJSONResponse
from starlette import status

from webapp.api.auth.router import auth_router
from webapp.crud.crud import update
from webapp.db.postgres import get_session
from webapp.schema.user import UserLogin, UserLoginResponse, USER_TABLE


@auth_router.post(
    '/update',
    response_model=UserLoginResponse,
)
async def update_user(user_id: int, body: UserLogin) -> ORJSONResponse:
    session = get_session()
    update(session, user_id, body, USER_TABLE)

    return ORJSONResponse(
        {
            'id': user_id,
            'username': body.username
        }
    )
