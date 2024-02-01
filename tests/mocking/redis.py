from typing import Dict


class TestRedisClient:
    redis_data: Dict[str, str] = {}

    async def set(self, key: str, payload: str, ex: None = None) -> None:
        self.redis_data[key] = payload

    async def get(self, key: str) -> str | None:
        return self.redis_data.get(key)

    async def delete(self, key: str) -> int:
        if key in self.redis_data:
            self.redis_data.pop(key)
            return 1
        return 0
