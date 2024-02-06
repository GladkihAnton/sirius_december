from typing import List

import orjson
from fastapi import Depends, HTTPException, Query, status
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from conf.config import settings
from webapp.api.education.router import lesson_router
from webapp.cache.key_builder import get_lesson_cache_key, get_lessons_by_course_cache_key
from webapp.crud.lesson import (
    create_lesson,
    delete_lesson,
    get_lesson_by_id,
    get_lessons_all_by_course_id,
    update_lesson,
)
from webapp.db.postgres import get_session
from webapp.db.redis import get_redis
from webapp.schema.education.lesson import LessonCreate, LessonRead
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@lesson_router.post('/', response_model=LessonRead, tags=['Lessons'], status_code=status.HTTP_201_CREATED)
async def create_lesson_endpoint(
    course_id: int,
    lesson_data: LessonCreate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
    redis: Redis = Depends(get_redis),
):
    if current_user['role'] not in ['admin', 'teacher']:
        raise HTTPException(status_code=403, detail='Нет доступа для выполнения этой операции')
    try:
        new_lesson = await create_lesson(session=session, course_id=course_id, lesson_data=lesson_data)
        # Инвалидация кэша для списка уроков курса
        cache_key_pattern = f'{settings.REDIS_SIRIUS_CACHE_PREFIX}:course:{course_id}:lessons:*'
        await redis.delete(*await redis.keys(cache_key_pattern))
        return new_lesson
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@lesson_router.get('/', response_model=List[LessonRead], tags=['Lessons'], response_class=ORJSONResponse)
async def get_all_lessons_by_course_endpoint(
    course_id: int,
    page: int = Query(1, ge=1, description='Номер страницы'),
    page_size: int = Query(10, ge=1, le=100, description='Количество уроков на странице'),
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
    redis: Redis = Depends(get_redis),
):
    cache_key = get_lessons_by_course_cache_key(course_id, page, page_size)
    cached_lessons = await redis.get(cache_key)

    if cached_lessons:
        return orjson.loads(cached_lessons)
    else:
        try:
            lessons = await get_lessons_all_by_course_id(
                session=session, course_id=course_id, page=page, page_size=page_size
            )
            if lessons is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Уроки не найдены')
            await redis.set(
                cache_key, orjson.dumps([lesson.dict() for lesson in lessons]), ex=3600
            )  # Кэширование на 1 час
            return lessons
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@lesson_router.get('/{lesson_id}', response_model=LessonRead, tags=['Lessons'])
async def get_lesson_endpoint(
    course_id: int,
    lesson_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
    redis: Redis = Depends(get_redis),
):
    cache_key = get_lesson_cache_key(lesson_id)
    cached_lesson = await redis.get(cache_key)

    if cached_lesson:
        return orjson.loads(cached_lesson)
    else:
        try:
            lesson = await get_lesson_by_id(session=session, course_id=course_id, lesson_id=lesson_id)
            if lesson is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Урок не найден')
            await redis.set(cache_key, orjson.dumps(lesson.dict()), ex=3600)  # Кэширование на 1 час
            return lesson
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@lesson_router.put('/{lesson_id}', response_model=LessonRead, tags=['Lessons'], response_class=ORJSONResponse)
async def update_lesson_endpoint(
    course_id: int,
    lesson_id: int,
    lesson_data: LessonCreate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
    redis: Redis = Depends(get_redis),
):
    if current_user['role'] in ['admin', 'teacher']:
        try:
            response = await update_lesson(
                session=session, course_id=course_id, lesson_id=lesson_id, lesson_data=lesson_data
            )
            if response is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Урок не найден')

            cache_key = get_lesson_cache_key(lesson_id)
            if cache_key:
                await redis.delete(cache_key)

            await redis.set(cache_key, response.json(), ex=3600)

            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав')


@lesson_router.delete('/{lesson_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Lessons'])
async def delete_lesson_endpoint(
    course_id: int,
    lesson_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
    redis: Redis = Depends(get_redis),
):
    if current_user['role'] not in ['admin', 'teacher']:
        raise HTTPException(status_code=403, detail='Нет доступа для выполнения этой операции')
    try:
        result = await delete_lesson(session=session, course_id=course_id, lesson_id=lesson_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Урок не найден')

        cache_key = get_lesson_cache_key(lesson_id)
        await redis.delete(cache_key)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
