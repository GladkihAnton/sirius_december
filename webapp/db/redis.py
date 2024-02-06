from redis.asyncio import Redis

redis: Redis


def get_redis() -> Redis:
    return redis
