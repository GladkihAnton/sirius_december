from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.task.router import task_router
from webapp.crud.task import get_task
from webapp.db.cache.cache import redis_get, redis_set
from webapp.db.postgres import get_session
from webapp.models.tms.task import Task
from webapp.schema.task.task import TaskResponse
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@task_router.get("/info/{task_id}", response_model=TaskResponse)
async def info(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    cached_task = await redis_get(Task.__tablename__, task_id)

    if cached_task:
        return ORJSONResponse(
            content={"result": cached_task}, status_code=status.HTTP_200_OK
        )

    task = await get_task(session, task_id)

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serializeble_obj = TaskResponse.model_validate(task).model_dump()

    await redis_set(Task.__tablename__, task.id, serializeble_obj)

    return ORJSONResponse(
        content={"result": serializeble_obj}, status_code=status.HTTP_200_OK
    )
