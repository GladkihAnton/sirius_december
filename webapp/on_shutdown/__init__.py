from typing import Optional

from redis.asyncio import Redis

from webapp.db import kafka

redis: Optional[Redis] = None


async def stop_producer() -> None:
    await kafka.producer.stop()


async def close_redis_pool() -> Optional[Redis]:
    """
    Закрывает пул подключений к Redis.
    Вызывается при остановке приложения.
    """
    global redis
    if redis:
        await redis.close()
    return None
