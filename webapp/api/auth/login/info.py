from fastapi import Depends
from fastapi.responses import ORJSONResponse

from webapp.api.auth.router import auth_router
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@auth_router.get("/info")
async def info(
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    return ORJSONResponse(access_token)
