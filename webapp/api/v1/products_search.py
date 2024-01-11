from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.v1.router import v1_router
from webapp.crud.product import get_products
from webapp.db.postgres import get_session
from webapp.schema.info.product import ProductInfo, ProductSearch, ProductsListResponse
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@v1_router.get('/products_search', response_model=ProductsListResponse)
async def products_search(
    body: ProductSearch,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    serialized_products = [
        ProductInfo.model_validate(product).model_dump() for product in await get_products(session, body)
    ]

    if not serialized_products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse({'products': serialized_products}, status_code=status.HTTP_200_OK)
