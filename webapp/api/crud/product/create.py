from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.product.router import product_router
from webapp.crud.product import product_crud
from webapp.db.postgres import get_session
from webapp.schema.info.product import ProductInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@product_router.post('/create')
async def create_product(
    body: ProductInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        await product_crud.create(session, body)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={'message': 'Product created successfully'}, status_code=status.HTTP_201_CREATED)
