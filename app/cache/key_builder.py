from app.core.config import Config


async def get_cache_name(model: str, model_id: int) -> str:
    return f"{Config.REDIS_CACHE_PREFIX}:{model}:{model_id}"
