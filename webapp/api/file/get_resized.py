import orjson
from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.file.router import file_router
from webapp.cache.key_builder import get_file_resize_cache
from webapp.crud.user_file import get_user_files
from webapp.db.postgres import get_session
from webapp.db.redis import get_redis
from webapp.schema.file.resize import ImageResizeResponse
from webapp.schema.file.resized import User
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth



@file_router.get('/resize', response_model=ImageResizeResponse)
async def get_resized(
    task_id: str,
    redis: Redis = Depends(get_redis),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    url_to_file: bytes = await redis.get(get_file_resize_cache(task_id))
    if url_to_file is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(orjson.loads(url_to_file))


@file_router.get('/resized_all', response_model=User)
async def get_resized_all(
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    result = await get_user_files(session, access_token['user_id'])

    return ORJSONResponse(User.model_validate(result).model_dump(mode='json'))
