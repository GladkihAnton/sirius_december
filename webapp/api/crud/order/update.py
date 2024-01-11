from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.order.router import order_router
from webapp.crud.order import order_crud
from webapp.db.postgres import get_session
from webapp.integrations.cache.cache import redis_drop_key
from webapp.models.sirius.order import Order
from webapp.schema.info.order import OrderInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@order_router.post('/update/{order_id}')
async def update_order(
    body: OrderInfo,
    order_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> Response:
    existing_order = await order_crud.get_model(session, order_id)

    if existing_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    updated_order = await order_crud.update(session, order_id, body)

    await redis_drop_key(Order.__name__, order_id)

    if updated_order:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(content={'message': 'Order created successfully'}, status_code=status.HTTP_201_CREATED)
