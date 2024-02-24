from conf.config import settings


def get_file_resize_cache(task_id: str) -> str:
    return f'{settings.REDIS_SIRIUS_CACHE_PREFIX}:file_resize:{task_id}'