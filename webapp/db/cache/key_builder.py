from conf.config import settings


async def get_cache_title(model: str, model_id: int) -> str:
    return f"{settings.REDIS_TMS_CACHE_PREFIX}:{model}:{model_id}"
