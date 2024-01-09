from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.category.router import category_router
from webapp.crud.task import create_task
from webapp.db.postgres import get_session
from webapp.schema.category.category import CategoryCreate
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@category_router.post(
    '/create'
)
async def category(
    body: CategoryCreate,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token)
) -> ORJSONResponse:
    user_id = access_token.get('user_id')
    try:
        await create_task(session, user_id, body)
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
