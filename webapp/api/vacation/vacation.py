from tkinter.tix import MAIN
from typing import List, Optional

import orjson
from fastapi import Depends, HTTPException, Query, status
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from conf.config import settings
from webapp.api.vacation.router import vacation_router
from webapp.cache.key_builder import (
    MAIN_KEY,
    get_vacation_cache_key,
    get_vacation_list_cache_key,
    get_vacation_pending_list_cache_key,
)
from webapp.crud.vacation import (
    create_vacation,
    delete_vacation,
    get_pending_vacations,
    get_vacation,
    get_vacations,
    update_vacation_approval,
)
from webapp.db.postgres import get_session
from webapp.db.redis import get_redis
from webapp.schema.login.user import User
from webapp.schema.vacation.vacation import (
    Vacation,
    VacationCreate,
    VacationRequst,
)
from webapp.utils.auth.user import get_current_user
from webapp.utils.decorator import measure_integration_latency


# Список всех отпусков
@measure_integration_latency(
    method_name='get_vacations_endpoint', integration_point='endpoint'
)
@vacation_router.get(
    '/',
    response_model=List[Vacation],
    tags=['Vacation'],
    response_class=ORJSONResponse,
)
async def get_vacations_endpoint(
    approved: Optional[bool] = None,
    skip: int = Query(0, alias='offset'),
    limit: int = Query(10, alias='limit'),
    session: AsyncSession = Depends(get_session),  # Получаем сеанс
    redis: Redis = Depends(get_redis),
) -> List[Vacation]:
    # Ключ кэша зависит от параметров запроса
    cache_key = get_vacation_list_cache_key(
        approved=approved, skip=skip, limit=limit
    )

    # Попытка получить данные из кэша
    cached_data = await redis.get(cache_key)
    if cached_data:
        # Десериализация данных из кэша и возврат
        return orjson.loads(cached_data)

    # Если данных нет в кэше, делаем запрос к базе данных
    vacations = await get_vacations(
        session=session, approved=approved, skip=skip, limit=limit
    )

    # Сериализация и сохранение данных в кэше
    await redis.hset(
        MAIN_KEY,
        cache_key,
        orjson.dumps([vac.model_dump() for vac in vacations]),
    )
    await redis.expire(MAIN_KEY, settings.CACHE_EXPIRATION_TIME)
    return vacations


# Список отпусков без статуса (ожидающие рассмотрения)
@measure_integration_latency(
    method_name='get_pending_vacations_endpoint', integration_point='endpoint'
)
@vacation_router.get(
    '/pending',
    response_model=List[Vacation],
    tags=['Vacation'],
    response_class=ORJSONResponse,
)
async def get_pending_vacations_endpoint(
    skip: int = Query(0, alias='offset'),
    limit: int = Query(10, alias='limit'),
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> List[Vacation]:
    cache_key = get_vacation_pending_list_cache_key(skip=skip, limit=limit)
    # Пытаемся получить данные из кэша по сгенерированному ключу
    cached_data = await redis.get(cache_key)

    # Если данные есть в кэше, возвращаем их
    if cached_data:
        return orjson.loads(cached_data)

    # Если данных нет в кэше, делаем запрос для получения отпусков без статуса
    pending_vacations = await get_pending_vacations(session, skip, limit)
    # Сохраняем полученные данные в кэше
    await redis.hset(
        MAIN_KEY,
        cache_key,
        orjson.dumps([vac.model_dump() for vac in pending_vacations]),
    )
    await redis.expire(MAIN_KEY, settings.CACHE_EXPIRATION_TIME)  # время жизни кэша
    return pending_vacations


# Детали отпуска по id
@measure_integration_latency(
    method_name='get_vacation_endpoint', integration_point='endpoint'
)
@vacation_router.get(
    '/{vacation_id}',
    response_model=Vacation,
    tags=['Vacation'],
    response_class=ORJSONResponse,
)
async def get_vacation_endpoint(
    vacation_id: int,
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> Vacation:
    cache_key = get_vacation_cache_key(vacation_id=vacation_id)
    cached_vacation = await redis.get(cache_key)

    if cached_vacation:
        return orjson.loads(cached_vacation)

    vacation = await get_vacation(session, vacation_id)
    if not vacation:
        raise HTTPException(status_code=404, detail='Vacation not found')
    await redis.hset(
        MAIN_KEY,
        cache_key,
        orjson.dumps(vacation.model_dump()),
    )
    await redis.expire(MAIN_KEY, settings.CACHE_EXPIRATION_TIME)
    return vacation


# Создание отпуска администратором
@measure_integration_latency(
    method_name='create_vacation_endpoint', integration_point='endpoint'
)
@vacation_router.post(
    '/',
    response_model=Vacation,
    status_code=status.HTTP_201_CREATED,
    tags=['Vacation'],
    response_class=ORJSONResponse,
)
async def create_vacation_endpoint(
    vacation_data: VacationCreate,  # Данные для создания нового отпуска
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> Vacation:
    new_vacation = await create_vacation(session, vacation_data.model_dump())
    # Удаление кэша, чтобы обновить данные
    await redis.delete(MAIN_KEY)
    return new_vacation


# Запрос на отпуск от сотрудника
@measure_integration_latency(
    method_name='vacation_request_endpoint', integration_point='endpoint'
)
@vacation_router.post(
    '/vacation-requests',
    response_model=Vacation,
    status_code=status.HTTP_201_CREATED,
    tags=['Vacation'],
    response_class=ORJSONResponse,
)
async def vacation_request_endpoint(
    vacation_request: VacationRequst,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> Vacation:
    vacation_data = vacation_request.model_dump()
    vacation_data['employee_id'] = current_user.id  # Установка id польз. в данные
    vacation_data['approved'] = None  # статус одобрения - ожидает рассмотрения

    new_vacation = await create_vacation(session, vacation_data)
    await redis.delete(MAIN_KEY)
    return new_vacation  # Возвращаем созданный отпуск


# Подтверждение/отклонение отпуска администратором
@measure_integration_latency(
    method_name='update_vacation_approval_endpoint',
    integration_point='endpoint',
)
@vacation_router.put(
    '/{vacation_id}/approval',
    response_model=Vacation,
    tags=['Vacation'],
    response_class=ORJSONResponse,
)
async def update_vacation_approval_endpoint(
    vacation_id: int,
    approved: bool,
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> (Vacation | None):
    updated_vacation = await update_vacation_approval(
        session, vacation_id, approved
    )
    # Инвалидируем кэш для этого отпуска
    cache_key = get_vacation_cache_key(vacation_id)
    await redis.delete(cache_key)  # Удаление кэша для указанного отпуска
    return updated_vacation


# Удаление отпуска
@measure_integration_latency(
    method_name='delete_vacation_endpoint', integration_point='endpoint'
)
@vacation_router.delete(
    '/{vacation_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Vacation'],
    response_class=ORJSONResponse,
)
async def delete_vacation_endpoint(
    vacation_id: int,
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> None:
    await delete_vacation(session, vacation_id)
    # Инвалидируем кэш для этого отпуска
    cache_key = get_vacation_cache_key(vacation_id)
    await redis.delete(cache_key)
    return None
