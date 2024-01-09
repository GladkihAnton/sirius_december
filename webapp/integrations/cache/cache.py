import json
from typing import Any

from conf.config import settings
from webapp.integrations.cache.key_builder import get_cache_title
from webapp.integrations.cache.redis import get_redis
from webapp.integrations.metrics.metrics import async_integrations_timer


@async_integrations_timer
async def redis_set(model: str, model_id: int, payload: Any) -> None:
    redis = get_redis()
    redis_key = await get_cache_title(model, model_id)
    await redis.set(redis_key, json.dumps(payload), ex=settings.FILE_EXPIRE_TIME)


@async_integrations_timer
async def redis_get(model: str, model_id: int) -> dict[str, str]:
    redis = get_redis()
    redis_key = await get_cache_title(model, model_id)
    cache = await redis.get(redis_key)
    if cache is None:
        return {}
    return json.loads(cache)