from typing import Any

from redis.asyncio import Redis

from webapp.integrations.cache.key_builder import get_cache_title

redis: Redis


def get_redis() -> Redis:
    global redis

    return redis


async def redis_set(model: str, model_id: int, payload: Any) -> None:
    global redis
    redis_key = await get_cache_title(model, model_id)
    await redis.set(redis_key, payload)
