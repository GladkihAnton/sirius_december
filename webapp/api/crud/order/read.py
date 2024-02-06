from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.order.router import order_router
from webapp.crud.order import order_crud
from webapp.db.postgres import get_session
from webapp.integrations.cache.cache import redis_get, redis_set
from webapp.models.sirius.order import Order
from webapp.schema.info.order import OrderInfo, OrderResponse, OrdersListResponse
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@order_router.get('/page/{page}', response_model=OrdersListResponse)
async def orders_get(
    page: int,
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    serialized_order = [
        OrderInfo.model_validate(order).model_dump() for order in await order_crud.get_page(session, page)
    ]
    return ORJSONResponse({'orders': serialized_order}, status_code=status.HTTP_200_OK)


@order_router.get('/{order_id}', response_model=OrderResponse)
async def get_cached_order(
    order_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if cached := (await redis_get(Order.__name__, order_id)):
        return ORJSONResponse({'cached_order': cached})

    order = await order_crud.get_model(session, order_id)

    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    serialized_order = OrderInfo(**order.__dict__).model_dump(mode='json')
    await redis_set(Order.__name__, order_id, serialized_order)

    return ORJSONResponse({'order': serialized_order}, status_code=status.HTTP_200_OK)
