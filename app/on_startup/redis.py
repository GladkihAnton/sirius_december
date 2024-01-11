from redis.asyncio import ConnectionPool, Redis

from app.core.config import Config
from app.db import redis


async def start_redis() -> None:
    pool = ConnectionPool(
        host=Config.REDIS_HOST,
        port=Config.REDIS_PORT,
        password=Config.REDIS_PASSWORD,
    )
    redis.redis = Redis(
        connection_pool=pool,
    )