from asyncio import QueueEmpty
from typing import Any, Dict

import msgpack
from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.delivery.product.router import product_router
from webapp.db.postgres import get_session
from webapp.db.rabbitmq import get_channel
from webapp.models.sirius.order import Order
from webapp.schema.order.base import OrderModel
from sqlalchemy.orm import joinedload

from webapp.utils.auth.jwt import JwtTokenT, validate_delivery


@product_router.get('/orders')
async def get_order(
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(validate_delivery),
) -> ORJSONResponse:
    channel = get_channel()

    queue_key = 'orders'

    queue = await channel.declare_queue(queue_key, auto_delete=False, durable=True, passive=True)

    try:
        body = (await queue.get(timeout=3, no_ack=False)).body
    except QueueEmpty:
        return _prepare_response({})

    order_id = msgpack.unpackb(body)['order_id']

    order = (await session.scalars(
        select(Order)
        .where(Order.id == order_id)
        .options(
            joinedload(Order.product),
            joinedload(Order.user),
        )
    )).one()

    return _prepare_response(OrderModel.model_validate(order).model_dump(mode='json'))


def _prepare_response(data: Dict[str, Any]) -> ORJSONResponse:
    return ORJSONResponse(
        {
            'data': data,
        }
    )