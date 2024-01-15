import orjson

from webapp.cache.key_builder import get_cache_name
from webapp.db.redis import get_redis
from webapp.metrics import async_integrations_timer


@async_integrations_timer
async def redis_get(key):
    redis = get_redis()
    redis_key = get_cache_name(key)
    cache = await redis.get(redis_key)
    if cache is None:
        return {}
    return orjson.loads(cache)


@async_integrations_timer
async def redis_set(key, value):
    redis = get_redis()
    redis_key = get_cache_name(key)
    await redis.set(redis_key, orjson.dumps(value))
