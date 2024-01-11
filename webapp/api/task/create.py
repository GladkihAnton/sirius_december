from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.task.router import task_router
from webapp.crud.task import create_task
from webapp.db.cache.cache import redis_set
from webapp.db.postgres import get_session
from webapp.models.tms.task import Task
from webapp.schema.task.task import TaskCreate, TaskResponse
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@task_router.post("/create")
async def create_task_handle(
    body: TaskCreate,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    user_id = access_token.get("user_id")
    try:
        task = await create_task(session, user_id, body)
        serializeble_obj = TaskResponse.model_validate(task).model_dump()

        await redis_set(Task.__tablename__, task.id, serializeble_obj)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return ORJSONResponse(
        content={"result": serializeble_obj},
        status_code=status.HTTP_201_CREATED
    )
