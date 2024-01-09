from fastapi import HTTPException
from starlette import status

from webapp.api.auth.router import auth_router
from webapp.crud.crud import delete
from webapp.db.postgres import get_session
from webapp.schema.user import USER_TABLE


@auth_router.post(
    '/delete',
    response_model=int,
)
async def delete_user(user_id: int) -> int:
    session = get_session()
    delete(session, user_id, USER_TABLE)
    
    return user_id
