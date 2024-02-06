from typing import List, Literal, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from webapp.models.sirius.employee import Employee
from webapp.models.sirius.vacation import Vacation
from webapp.schema.employee.employee import (
    Employee as EmployeePydantic,
    EmployeeCreate,
)
from webapp.utils.decorator import measure_integration_latency


# Получение сотрудника по ID
@measure_integration_latency(
    method_name='get_employee', integration_point='database'
)
async def get_employee(
    session: AsyncSession, employee_id: int
) -> EmployeePydantic:
    result = await session.execute(
        select(Employee)
        .options(selectinload(Employee.vacations))
        .where(Employee.id == employee_id)
    )
    employee = result.unique().scalars().one_or_none()
    return EmployeePydantic.model_validate(employee)


# Получение всех сотрудников с возможными параметрами
# пропуска и ограничения для пагинации
@measure_integration_latency(
    method_name='get_employees', integration_point='database'
)
async def get_employees(
    session: AsyncSession, skip: int, limit: int
) -> List[EmployeePydantic]:
    result = await session.execute(
        select(Employee)
        .options(selectinload(Employee.vacations))
        .offset(skip)
        .limit(limit)
    )
    employees = result.unique().scalars().all()
    return [EmployeePydantic.model_validate(emp) for emp in employees]


# Создание нового сотрудника
@measure_integration_latency(
    method_name='create_employee', integration_point='database'
)
async def create_employee(
    session: AsyncSession, employee_data: EmployeeCreate
) -> EmployeeCreate:
    # Преобразуем Pydantic модель в словарь, исключая неустановленные поля,
    # и создаем объект Employee, который является моделью SQLAlchemy
    new_employee = Employee(**employee_data.model_dump(exclude_unset=True))
    session.add(new_employee)
    await session.commit()
    await session.refresh(new_employee)
    # Возвращаем созданный объект Employee
    return new_employee


# Обновление существующего сотрудника
@measure_integration_latency(
    method_name='update_employee', integration_point='database'
)
async def update_employee(
    session: AsyncSession, employee_id: int, update_data: dict[str, bool]
) -> (Employee | None):
    result = await session.execute(
        select(Employee)
        .options(selectinload(Employee.vacations))
        .where(Employee.id == employee_id)
    )
    employee = result.unique().scalars().one_or_none()
    if employee:
        for key, value in update_data.items():
            setattr(employee, key, value)
        await session.commit()
        await session.refresh(employee, attribute_names=['vacations'])
    return employee


# Получение всех отпусков для конкретного сотрудника
@measure_integration_latency(
    method_name='get_vacations_for_employee', integration_point='database'
)
async def get_vacations_for_employee(
    session: AsyncSession, employee_id: int, skip: int, limit: int
) -> Sequence[Vacation]:
    result = await session.execute(
        select(Vacation)
        .where(Vacation.employee_id == employee_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


# Удаление сотрудника
@measure_integration_latency(
    method_name='delete_employee', integration_point='database'
)
async def delete_employee(
    session: AsyncSession, employee_id: int
) -> Literal[True]:
    result = await session.execute(
        select(Employee).where(Employee.id == employee_id)
    )
    employee = result.scalars().one_or_none()
    if employee:
        await session.delete(employee)
        await session.commit()
    return True
