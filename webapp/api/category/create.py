from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.category.router import category_router
from webapp.crud.category import create_category
from webapp.db.cache.cache import redis_set
from webapp.db.postgres import get_session
from webapp.models.tms.category import Category
from webapp.schema.category.category import CategoryCreate, CategoryResponse
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@category_router.post("/create", response_model=CategoryResponse)
async def create_category_handle(
    body: CategoryCreate,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        category = await create_category(session, body)
        serializeble_obj = CategoryResponse.model_validate(category).model_dump()

        await redis_set(Category.__tablename__, category.id, serializeble_obj)

        return ORJSONResponse(
            content={"result": serializeble_obj},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
