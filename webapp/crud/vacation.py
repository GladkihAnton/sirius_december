from typing import List, Literal, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.sirius.vacation import Vacation
from webapp.schema.vacation.vacation import Vacation as VacationPydantic
from webapp.utils.decorator import measure_integration_latency


# Получение отпуска по ID
@measure_integration_latency(
    method_name='get_vacation', integration_point='database'
)
async def get_vacation(
    session: AsyncSession, vacation_id: int
) -> Optional[VacationPydantic]:
    result = await session.execute(
        select(Vacation).where(Vacation.id == vacation_id)
    )
    vacation = result.scalars().one_or_none()
    return VacationPydantic.model_validate(vacation)


# Получение всех отпусков со статусами
@measure_integration_latency(
    method_name='get_vacations', integration_point='database'
)
async def get_vacations(
    session: AsyncSession,
    skip: int,
    limit: int,
    approved: Optional[bool] = None,
) -> List[VacationPydantic]:
    query = select(Vacation)
    if approved is not None:
        query = query.where(Vacation.approved == approved)
    else:
        query = query.where(Vacation.approved.isnot(None))

    results = await session.execute(query.offset(skip).limit(limit))
    vacations = results.scalars().all()
    return [
        VacationPydantic.model_validate(vacation) for vacation in vacations
    ]


# Получение списка отпусков без статуса (ожидающие рассмотрения)
@measure_integration_latency(
    method_name='get_pending_vacations', integration_point='database'
)
async def get_pending_vacations(
    session: AsyncSession, skip: int = 0, limit: int = 10
) -> List[VacationPydantic]:
    query = select(Vacation).where(Vacation.approved.is_(None))
    results = await session.execute(query.offset(skip).limit(limit))
    vacations = results.scalars().all()
    return [
        VacationPydantic.model_validate(vacation) for vacation in vacations
    ]


# Создание нового отпуска
@measure_integration_latency(
    method_name='create_vacation', integration_point='database'
)
async def create_vacation(
    session: AsyncSession, vacation_data: dict[str, bool]
) -> VacationPydantic:
    new_vacation = Vacation(**vacation_data)
    session.add(new_vacation)
    await session.commit()
    await session.refresh(new_vacation)
    return VacationPydantic.model_validate(new_vacation)


# Удаление отпуска
@measure_integration_latency(
    method_name='delete_vacation', integration_point='database'
)
async def delete_vacation(
    session: AsyncSession, vacation_id: int
) -> Literal[True]:
    result = await session.execute(
        select(Vacation).where(Vacation.id == vacation_id)
    )
    vacation = result.scalars().one_or_none()
    if vacation:
        await session.delete(vacation)
        await session.commit()
    return True


# Обновление статуса отпуска (approved)
@measure_integration_latency(
    method_name='update_vacation_approval', integration_point='database'
)
async def update_vacation_approval(
    session: AsyncSession, vacation_id: int, approved: bool
) -> Optional[VacationPydantic]:
    await session.execute(
        update(Vacation)
        .where(Vacation.id == vacation_id)
        .values(approved=approved)
        .execution_options(synchronize_session='fetch')
    )
    await session.commit()
    updated_vacation = await get_vacation(
        session, vacation_id
    )  # Используем уже изменённую функцию get_vacation
    return (
        VacationPydantic.model_validate(updated_vacation)
        if updated_vacation
        else None
    )
