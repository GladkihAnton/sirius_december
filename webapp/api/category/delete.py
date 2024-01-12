from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.category.router import category_router
from webapp.crud.category import delete_category, get_category
from webapp.db.cache.cache import redis_drop_key
from webapp.db.postgres import get_session
from webapp.models.tms.category import Category
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@category_router.delete("/delete/{category_id}")
async def delete_category_handle(
    category_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> Response:
    category_to_delete = await get_category(session, category_id)

    if category_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await delete_category(session, category_to_delete)

    await redis_drop_key(Category.__tablename__, category_to_delete.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
