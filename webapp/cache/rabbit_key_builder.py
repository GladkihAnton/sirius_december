from conf.config import settings


def get_user_products_queue_key(user_id: int) -> str:
    return f'{settings.RABBIT_SIRIUS_USER_PREFIX}:{user_id}'