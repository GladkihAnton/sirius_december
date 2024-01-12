from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.tms.task import Task
from webapp.schema.task.task import TaskCreate, TaskUpdate


async def get_task(session: AsyncSession, task_id: int) -> Task | None:
    return (
        await session.scalars(
            select(Task).where(
                Task.id == task_id,
            )
        )
    ).one_or_none()


async def create_task(
    session: AsyncSession, user_id: int, task_info: TaskCreate
) -> Task:
    new_task = Task(
        title=task_info.title,
        description=task_info.description,
        deadline=task_info.deadline,
        category_id=task_info.category_id,
        creator_id=user_id,
        receiver_id=task_info.receiver_id,
    )

    session.add(new_task)
    await session.commit()

    return new_task


async def delete_task(session: AsyncSession, task: Task) -> None:
    await session.delete(task)
    await session.commit()

    return None


async def update_task(session: AsyncSession, task: Task, task_info: TaskUpdate) -> Task:
    for key, value in task_info.model_dump().items():
        if value is not None:
            setattr(task, key, value)

    await session.commit()

    return task
