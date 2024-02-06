from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.product.router import product_router
from webapp.crud.product import product_crud
from webapp.db.postgres import get_session
from webapp.integrations.cache.cache import redis_drop_key
from webapp.models.sirius.product import Product
from webapp.schema.info.product import ProductInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@product_router.post('/update/{product_id}')
async def update_product(
    body: ProductInfo,
    product_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> Response:
    existing_product = await product_crud.get_model(session, product_id)

    if existing_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    updated_product = await product_crud.update(session, product_id, body)

    await redis_drop_key(Product.__name__, product_id)

    if updated_product:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(content={'message': 'Product created successfully'}, status_code=status.HTTP_201_CREATED)
