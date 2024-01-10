from typing import Dict


class TestRedisClient:
    redis_data: Dict[str, str] = {}

    @classmethod
    async def set(cls, key: str, payload: str, ex: None = None) -> None:
        cls.redis_data[key] = payload

    @classmethod
    async def get(cls, key: str) -> str | None:
        return cls.redis_data.get(key)

    @classmethod
    async def delete(cls, key: str) -> int:
        if key in cls.redis_data:
            cls.redis_data.pop(key)
            return 1
        return 0
