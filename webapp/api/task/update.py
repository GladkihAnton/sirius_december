from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.task.router import task_router
from webapp.crud.task import get_task, update_task
from webapp.db.cache.cache import redis_drop_key
from webapp.db.postgres import get_session
from webapp.models.tms.task import Task
from webapp.schema.task.task import TaskResponse, TaskUpdate
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@task_router.put("/update/{task_id}", response_model=TaskResponse)
async def update_task_handle(
    task_id: int,
    body: TaskUpdate,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    task_to_update = await get_task(session, task_id)

    if task_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    updated_task = await update_task(session, task_to_update, body)

    await redis_drop_key(Task.__tablename__, task_to_update.id)

    return ORJSONResponse(
        content={"result": TaskResponse.model_validate(updated_task).model_dump()},
        status_code=status.HTTP_200_OK,
    )
