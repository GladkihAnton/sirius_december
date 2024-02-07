from fastapi import HTTPException
from fastapi.responses import ORJSONResponse
from starlette import status

from webapp.api.auth.router import auth_router
from webapp.cache.redis import redis_get
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@auth_router.post(
    '/info',
    response_model=JwtTokenT,
)
async def info() -> ORJSONResponse:
    access_token: bytes = await redis_get('access_token')
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    token = jwt_auth.validate_token(access_token)
    return ORJSONResponse(token)
