from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.category.router import category_router
from webapp.crud.category import get_category, update_category
from webapp.db.cache.cache import redis_drop_key
from webapp.db.postgres import get_session
from webapp.models.tms.category import Category
from webapp.schema.category.category import CategoryResponse, CategoryUpdate
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@category_router.put("/update/{category_id}", response_model=CategoryResponse)
async def update_category_handle(
    category_id: int,
    body: CategoryUpdate,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    category_to_update = await get_category(session, category_id)

    if category_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    updated_category = await update_category(session, category_to_update, body)

    await redis_drop_key(Category.__tablename__, category_to_update.id)

    return ORJSONResponse(
        content={
            "result": CategoryResponse.model_validate(updated_category).model_dump()
        },
        status_code=status.HTTP_200_OK,
    )
