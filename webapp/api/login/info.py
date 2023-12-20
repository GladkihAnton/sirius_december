from fastapi import Depends
from fastapi.responses import ORJSONResponse

from webapp.api.login.router import auth_router
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@auth_router.post(
    '/info',
    response_model=JwtTokenT,
)
async def info(
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    return ORJSONResponse(access_token)
