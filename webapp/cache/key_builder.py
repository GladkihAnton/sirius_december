from conf.config import settings


async def get_cache_name(model: str, model_id: int) -> str:
    return f"{settings.REDIS_CACHE_PREFIX}:{model}:{model_id}"
