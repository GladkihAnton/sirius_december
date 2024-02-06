from conf.config import settings


def get_course_cache_key(course_id: int) -> str:
    return f'{settings.REDIS_SIRIUS_CACHE_PREFIX}:course:{course_id}'


def get_courses_page_cache_key(page: int, page_size: int) -> str:
    return f'{settings.REDIS_SIRIUS_CACHE_PREFIX}:courses:page_{page}:size_{page_size}'


def get_lesson_cache_key(lesson_id: int) -> str:
    return f'{settings.REDIS_SIRIUS_CACHE_PREFIX}:lesson:{lesson_id}'


def get_lessons_by_course_cache_key(course_id: int, page: int, page_size: int) -> str:
    return f'{settings.REDIS_SIRIUS_CACHE_PREFIX}:course:{course_id}:lessons:page_{page}_size_{page_size}'


def get_files_by_lesson_cache_key(course_id: int, lesson_id: int, page: int, page_size: int) -> str:
    return (
        f'{settings.REDIS_SIRIUS_CACHE_PREFIX}:course_{course_id}:lesson_{lesson_id}:files:page_{page}:size_{page_size}'
    )
