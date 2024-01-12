from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.category.router import category_router
from webapp.crud.category import get_category
from webapp.db.cache.cache import redis_get, redis_set
from webapp.db.postgres import get_session
from webapp.models.tms.category import Category
from webapp.schema.category.category import CategoryResponse
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@category_router.get("/info/{category_id}", response_model=CategoryResponse)
async def info(
    category_id: int,
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    cached_category = await redis_get(Category.__tablename__, category_id)

    if cached_category:
        return ORJSONResponse(
            content={"result": cached_category}, status_code=status.HTTP_200_OK
        )

    category = await get_category(session, category_id)

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serializeble_obj = CategoryResponse.model_validate(category).model_dump()

    await redis_set(Category.__tablename__, category.id, serializeble_obj)

    return ORJSONResponse(
        content={"result": serializeble_obj}, status_code=status.HTTP_200_OK
    )
