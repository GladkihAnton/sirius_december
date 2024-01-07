from typing import Dict


class TestRedisClient:
    redis_data: Dict[str, str] = {}

    @classmethod
    async def set(cls, key: str, payload: str, ex: None = None) -> None:
        cls.redis_data[key] = payload

    @classmethod
    async def get(cls, key: str) -> str | None:
        return cls.redis_data.get(key)
