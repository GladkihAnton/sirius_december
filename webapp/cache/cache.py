from typing import Any

import orjson

from webapp.cache.key_builder import get_cache_key
from webapp.db.redis import get_redis
from webapp.metrics.metrics import INTEGRATIONS_LATENCY


@INTEGRATIONS_LATENCY.time()
async def redis_set(model: str, model_id: int, data: Any) -> None:
    redis = get_redis()
    key = await get_cache_key(model, model_id)
    await redis.set(key, orjson.dumps(data))


@INTEGRATIONS_LATENCY.time()
async def redis_get(model: str, model_id: int) -> Any:
    redis = get_redis()
    key = await get_cache_key(model, model_id)
    cached = await redis.get(key)

    if cached is None:
        return None

    return orjson.loads(cached)


@INTEGRATIONS_LATENCY.time()
async def redis_remove(model: str, model_id: int) -> None:
    redis = get_redis()
    key = await get_cache_key(model, model_id)
    await redis.delete(key)
