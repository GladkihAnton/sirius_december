from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.db.postgres import get_session
from webapp.api.task.router import task_router
from webapp.crud.task import get_task
from webapp.schema.task.task import TaskResponse


@task_router.get(
    '/info',
    response_model=TaskResponse
)
async def info(
    task_id: int,
    session: AsyncSession = Depends(get_session)
) -> ORJSONResponse:
    task = await get_task(session, task_id)

    if task is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return ORJSONResponse(content={'result': task.__dict__})
