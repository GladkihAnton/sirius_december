from datetime import timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from conf.config import settings
from webapp.api.auth.router import auth_router
from webapp.integrations.postgres import get_session
from webapp.utils.auth.jwt import authenticate_user, create_access_token, oauth2_scheme

@auth_router.post('/info')
async def info(
    access_token: Annotated[str, Depends(oauth2_scheme)],
) -> ORJSONResponse:
    return ORJSONResponse(access_token)