from typing import Any

import orjson
import uuid

from app.cache.key_builder import get_cache_name
from app.core.config import Config
from app.db.redis import get_redis
from app.metrics.metrics import async_integrations_timer


@async_integrations_timer
async def redis_set(model: str, model_id: uuid.UUID | str, payload: Any) -> None:
    redis = get_redis()
    redis_key = await get_cache_name(model, model_id)
    await redis.set(redis_key, orjson.dumps(payload), ex=Config.REDIS_EXPIRE_TIME)


@async_integrations_timer
async def redis_get(model: str, model_id: uuid.UUID | str) -> dict[str, str]:
    redis = get_redis()
    redis_key = await get_cache_name(model, model_id)
    cache = await redis.get(redis_key)
    if cache is None:
        return {}
    return orjson.loads(cache)


@async_integrations_timer
async def redis_drop_key(model: str, model_id: uuid.UUID | str) -> None:
    redis = get_redis()
    redis_key = await get_cache_name(model, model_id)
    await redis.delete(redis_key)
