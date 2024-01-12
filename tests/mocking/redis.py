from typing import Any, Dict


class TestRedisClient:
    redis_storage: Dict[str, dict] = {}

    @classmethod
    async def set(cls, name: str, value: Dict[str, Any]) -> None:
        cls.redis_storage[name] = value

    @classmethod
    async def get(cls, name: str) -> Dict[str, Any] | None:
        return cls.redis_storage.get(name)

    @classmethod
    async def delete(cls, name: str) -> None:
        cls.redis_storage.pop(name, None)
