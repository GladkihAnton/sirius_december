from typing import Annotated

from fastapi import Depends
from fastapi.responses import ORJSONResponse

from webapp.api.auth.router import auth_router
from webapp.utils.auth.jwt import oauth2_scheme

@auth_router.post('/info')
async def info(
    access_token: Annotated[str, Depends(oauth2_scheme)],
) -> ORJSONResponse:
    return ORJSONResponse(access_token)