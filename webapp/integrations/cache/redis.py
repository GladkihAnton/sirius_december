from redis.asyncio import Redis

redis: Redis


def get_redis() -> Redis:
    global redis

    return redis
