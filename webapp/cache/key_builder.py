from conf.config import settings


def get_cache_name(task_id: str) -> str:
    return f'{settings.REDIS_SIRIUS_CACHE_PREFIX}:info:{task_id}'
