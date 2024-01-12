from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.task.router import task_router
from webapp.crud.task import delete_task, get_task
from webapp.db.cache.cache import redis_drop_key
from webapp.db.postgres import get_session
from webapp.models.tms.task import Task
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@task_router.delete("/delete/{task_id}")
async def delete_task_handle(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> Response:
    task_to_delete = await get_task(session, task_id)

    if task_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await delete_task(session, task_to_delete)

    await redis_drop_key(Task.__tablename__, task_to_delete.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
