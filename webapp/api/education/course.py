from typing import List

import orjson
from fastapi import Depends, HTTPException, Query
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.education.router import course_router
from webapp.cache.key_builder import get_course_cache_key, get_courses_page_cache_key
from webapp.crud.course import create_course, delete_course, get_course_by_id, get_courses_all, update_course
from webapp.crud.subscribe import create_subscription
from webapp.crud.user import UserRead, get_course_subscribers
from webapp.db.postgres import get_session
from webapp.db.redis import get_redis
from webapp.schema.education.course import CourseCreate, CourseRead
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@course_router.post(
    '/', response_model=CourseRead, status_code=status.HTTP_201_CREATED, tags=['Courses'], response_class=ORJSONResponse
)
async def create_course_endpoint(
    course_data: CourseCreate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    if current_user['role'] in ['admin', 'teacher']:
        try:
            return await create_course(session=session, course_data=course_data)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ошибка при создании курса'
            ) from e
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав')


@course_router.get('/', response_model=List[CourseRead], tags=['Courses'], response_class=ORJSONResponse)
async def get_all_courses_endpoint(
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
    page: int = Query(1, ge=1, description='Номер страницы'),
    page_size: int = Query(10, ge=1, le=100, description='Количество курсов на странице'),
    redis: Redis = Depends(get_redis),
):
    cache_key = get_courses_page_cache_key(page, page_size)
    cached_courses = await redis.get(cache_key)
    if cached_courses:
        return orjson.loads(cached_courses)
    else:
        try:
            courses = await get_courses_all(session=session, page=page, page_size=page_size)
            if courses:
                await redis.set(cache_key, orjson.dumps([course.dict() for course in courses]), ex=3600)  # Кэш на 1 час
            return courses
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ошибка при получении списка курсов'
            ) from e


@course_router.get('/{course_id}', response_model=CourseRead, tags=['Courses'], response_class=ORJSONResponse)
async def get_course_endpoint(
    course_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
    redis: Redis = Depends(get_redis),
):
    cache_key = get_course_cache_key(course_id)

    cached_course = await redis.get(cache_key)

    if cached_course:
        return orjson.loads(cached_course)
    else:
        try:
            response = await get_course_by_id(session=session, course_id=course_id)
            if response is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found')

            await redis.set(cache_key, response.json(), ex=3600)

            return response
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Database error') from e
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@course_router.put('/{course_id}', response_model=CourseRead, tags=['Courses'], response_class=ORJSONResponse)
async def update_course_endpoint(
    course_id: int,
    course_data: CourseCreate,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
    redis: Redis = Depends(get_redis),
):
    if current_user['role'] in ['admin', 'teacher']:
        try:
            response = await update_course(session=session, course_id=course_id, course_data=course_data)
            if response is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Курс не найден')

            cache_key = get_course_cache_key(course_id)
            await redis.delete(cache_key)

            await redis.set(cache_key, response.json(), ex=3600)

            return response
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ошибка при обновлении курса'
            ) from e
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав')


@course_router.get(
    '/{course_id}/subscribers', response_model=List[UserRead], response_class=ORJSONResponse, tags=['Courses']
)
async def get_course_subscribers_endpoint(
    course_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    courses = await get_course_subscribers(session=session, course_id=course_id)
    if courses:
        return courses
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Подписчиков не найдено')


@course_router.post('/{course_id}/subscribe', status_code=status.HTTP_201_CREATED, tags=['Courses'])
async def get_course_subscribe_endpoint(
    course_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
):
    try:
        return await create_subscription(session=session, course_id=course_id, user_id=current_user['user_id'])
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ошибка при подписке') from e


@course_router.delete(
    '/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'], response_class=ORJSONResponse
)
async def delete_course_endpoint(
    course_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: JwtTokenT = Depends(jwt_auth.get_current_user),
    redis: Redis = Depends(get_redis),
):
    if current_user['role'] in ['admin', 'teacher']:
        try:
            result = await delete_course(session=session, course_id=course_id)
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Курс не найден')

            cache_key = get_course_cache_key(course_id)
            await redis.delete(cache_key)

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ошибка при удалении курса'
            ) from e
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав')
