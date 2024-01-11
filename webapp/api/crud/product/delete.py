from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.product.router import product_router
from webapp.crud.product import product_crud
from webapp.db.postgres import get_session
from webapp.integrations.cache.cache import redis_drop_key
from webapp.models.sirius.product import Product
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@product_router.post('/delete/{product_id}')
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> Response:
    if not await product_crud.delete(session, product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await redis_drop_key(Product.__name__, product_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
