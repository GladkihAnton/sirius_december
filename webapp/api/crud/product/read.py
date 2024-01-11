from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.product.router import product_router
from webapp.crud.product import product_crud
from webapp.db.postgres import get_session
from webapp.integrations.cache.cache import redis_get, redis_set
from webapp.models.sirius.product import Product
from webapp.schema.info.product import ProductInfo, ProductResponse, ProductsListResponse
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@product_router.get('/page/{page}', response_model=ProductsListResponse)
async def products_get(
    page: int,
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    serialized_products = [
        ProductInfo.model_validate(product).model_dump() for product in await product_crud.get_page(session, page)
    ]
    return ORJSONResponse({'products': serialized_products}, status_code=status.HTTP_200_OK)


@product_router.get('/{product_id}', response_model=ProductResponse)
async def get_cached_product(
    product_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if cached := (await redis_get(Product.__name__, product_id)):
        return ORJSONResponse({'cached_product': cached})

    product = await product_crud.get_model(session, product_id)

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    serialized_product = ProductInfo(**product.__dict__).model_dump(mode='json')
    await redis_set(Product.__name__, product_id, serialized_product)

    return ORJSONResponse({'product': serialized_product}, status_code=status.HTTP_200_OK)
