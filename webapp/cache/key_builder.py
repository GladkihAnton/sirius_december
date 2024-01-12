from conf.config import settings


async def get_cache_key(model: str, model_id: int) -> str:
    return f'{settings.REDIS_SIRIUS_CACHE_PREFIX}:{model}:{model_id}'
