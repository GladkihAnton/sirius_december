from conf.config import settings


def get_employee_cache_key(employee_id: int) -> str:
    return f'{settings.REDIS_SIRIUS_CACHE_PREFIX}:employee_cache:{employee_id}'


def get_vacation_cache_key(vacation_id: int) -> str:
    return f'{settings.REDIS_SIRIUS_CACHE_PREFIX}:vacation_cache:{vacation_id}'
