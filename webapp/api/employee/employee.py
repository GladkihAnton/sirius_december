from typing import List, Sequence

import orjson
from fastapi import Depends, HTTPException, Query, status
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from conf.config import settings
from webapp.api.employee.router import employee_router
from webapp.cache.key_builder import get_employee_cache_key
from webapp.crud.employee import (
    create_employee,
    delete_employee,
    get_employee,
    get_employees,
    get_vacations_for_employee,
    update_employee,
)
from webapp.db.postgres import get_session
from webapp.db.redis import get_redis
from webapp.schema.employee.employee import (
    Employee,
    EmployeeCreate,
    EmployeeUpdate,
)
from webapp.schema.vacation.vacation import Vacation
from webapp.utils.decorator import measure_integration_latency


# Создание учетной записи сотрудника
@measure_integration_latency(
    method_name='create_employee_endpoint', integration_point='endpoint'
)
@employee_router.post(
    '/',
    response_model=EmployeeCreate,
    status_code=status.HTTP_201_CREATED,
    tags=['Employee'],
    response_class=ORJSONResponse,
)
async def create_employee_endpoint(
    employee_data: EmployeeCreate,
    session: AsyncSession = Depends(get_session),
) -> EmployeeCreate:
    created_employee = await create_employee(
        session=session, employee_data=employee_data
    )
    return created_employee


# Список всех сотрудников
@measure_integration_latency(
    method_name='get_employees_endpoint', integration_point='endpoint'
)
@employee_router.get(
    '/',
    response_model=List[Employee],
    tags=['Employee'],
    response_class=ORJSONResponse,
)
async def get_employees_endpoint(
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, alias='offset'),
    limit: int = Query(10, alias='limit'),
    redis: Redis = Depends(get_redis),
) -> List[Employee]:
    # Проверяем наличие данных в кэше
    cache_key = f'employee_{skip}_{limit}'
    cached_data = await redis.get(cache_key)

    # Если есть данные в кэше, то возвращаем их
    if cached_data:
        # Десериализуем данные из байтов в Python-объект
        # Возвращаем десериализованные данные в ответе
        return orjson.loads(cached_data)

    # Если данных нет в кэше, делаем запрос к базе данных
    employees = await get_employees(session=session, skip=skip, limit=limit)
    # Сохраняем данные в кэше
    await redis.set(
        cache_key,
        orjson.dumps([emp.model_dump() for emp in employees]),
        ex=settings.CACHE_EXPIRATION_TIME,
    )

    return employees


# Изменение учетных данных сотрудника (частичное обновление)
@measure_integration_latency(
    method_name='patch_employee_endpoint', integration_point='endpoint'
)
@employee_router.patch(
    '/{employee_id}',
    response_model=Employee,
    tags=['Employee'],
    response_class=ORJSONResponse,
)
async def patch_employee_endpoint(
    employee_id: int,
    employee_data: EmployeeUpdate,
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),  # Добавляем Redis
) -> Employee:
    # Очищаем кэш сотрудника, так как данные обновляются
    cache_key = get_employee_cache_key(employee_id)
    await redis.delete(cache_key)

    return await update_employee(
        session=session,
        employee_id=employee_id,
        update_data=employee_data.model_dump(exclude_unset=True),
    )


# Список отпусков для конкретного сотрудника
@measure_integration_latency(
    method_name='get_vacations_for_employee_endpoint',
    integration_point='endpoint',
)
@employee_router.get(
    '/{employee_id}/vacations',
    response_model=List[Vacation],
    tags=['Employee'],
    response_class=ORJSONResponse,
)
async def get_vacations_for_employee_endpoint(
    employee_id: int,
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, alias='offset'),
    limit: int = Query(10, alias='limit'),
) -> Sequence[Vacation]:
    return await get_vacations_for_employee(
        session=session, employee_id=employee_id, skip=skip, limit=limit
    )


# Информация о сотруднике
@measure_integration_latency(
    method_name='get_employee_endpoint', integration_point='endpoint'
)
@employee_router.get(
    '/{employee_id}',
    response_model=Employee,
    tags=['Employee'],
    response_class=ORJSONResponse,
)
async def get_employee_endpoint(
    employee_id: int,
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),  # Добавляем Redis
) -> Employee:
    # Проверяем наличие данных о сотруднике в кэше
    cache_key = get_employee_cache_key(employee_id)
    cached_data = await redis.get(cache_key)

    if cached_data:
        # Десериализуем данные из байтов в Python-объект
        employees = orjson.loads(cached_data)
        # Возвращаем десериализованные данные в ответе
        return employees

    # Если данных нет в кэше, делаем запрос к базе данных
    employee = await get_employee(session=session, employee_id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail='Employee not found')

    # Сохраняем данные о сотруднике в кэше
    await redis.set(
        cache_key,
        employee.model_dump_json(),
        ex=settings.CACHE_EXPIRATION_TIME,
    )

    return employee


# Удаление сотрудника
@measure_integration_latency(
    method_name='delete_employee_endpoint', integration_point='endpoint'
)
@employee_router.delete(
    '/{employee_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Employee'],
    response_class=ORJSONResponse,
)
async def delete_employee_endpoint(
    employee_id: int,
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),  # Добавляем Redis
) -> None:
    # Очищаем кэш сотрудника перед удалением
    cache_key = get_employee_cache_key(employee_id)
    await redis.delete(cache_key)

    employee = await delete_employee(session=session, employee_id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail='Employee not found')

    # Возвращаем статус 204 No Content и сообщение об успешном удалении
    return None
