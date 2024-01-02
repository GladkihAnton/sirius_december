from typing import Dict


class TestRedisClient:
    def __init__(self, redis_data: Dict[str, str]) -> None:
        self.redis_data: Dict[str, str] = redis_data

    async def set(self, key: str, value: str, ex: None = None) -> None:
        self.redis_data[key] = value

    async def get(self, key: str) -> str | None:
        return self.redis_data.get(key)
