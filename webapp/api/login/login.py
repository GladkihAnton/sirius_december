from typing import Any, Dict

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.login.router import auth_router
from webapp.db.postgres import get_session
from webapp.utils.auth.jwt import jwt_auth


@auth_router.post('/login')
async def login(session: AsyncSession = Depends(get_session)) -> Dict[str, Any]:
    user_id = 1
    return {
        'access_token': jwt_auth.create_token(user_id),
    }
