from redis.asyncio import ConnectionPool, Redis

from conf.config import settings
from webapp.db import redis


async def start_redis() -> None:
    pool = ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
    )
    redis.redis = Redis(
        connection_pool=pool,
    )

