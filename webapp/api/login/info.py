from typing import Any, Dict

from fastapi import Depends

from webapp.api.login.router import auth_router
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@auth_router.post('/info')
async def info(
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> Dict[str, Any]:
    return access_token
