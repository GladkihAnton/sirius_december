from typing import Any, Dict

import msgpack
from aio_pika import Message
from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.customer.product.router import product_router
from webapp.db.postgres import get_session
from webapp.db.rabbitmq import get_exchange_orders
from webapp.models.sirius.order import Order
from webapp.models.sirius.user_product_feedback import UserProductFeedBack, StatusFeedbackEnum
from webapp.utils.auth.jwt import JwtTokenT, validate_customer


@product_router.post('/order')
async def create_order(
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(validate_customer),
) -> ORJSONResponse:
    async with session.begin():
        order_ids = (await session.execute(
            insert(Order)
            .from_select(
                [UserProductFeedBack.user_id, UserProductFeedBack.product_id],
                select(UserProductFeedBack.user_id, UserProductFeedBack.product_id)
                .where(
                    UserProductFeedBack.user_id == access_token['user_id'],
                    UserProductFeedBack.status == StatusFeedbackEnum.liked,
                )
            )
            .on_conflict_do_nothing()
            .returning(Order.id)
        )).scalars().all()

        await session.execute(
            update(UserProductFeedBack)
            .values(status=StatusFeedbackEnum.added_to_order)
            .where(
                UserProductFeedBack.user_id == access_token['user_id'],
                UserProductFeedBack.status == StatusFeedbackEnum.liked,
            )
        )

    exchange_orders = get_exchange_orders()
    for order_id in order_ids:
        await exchange_orders.publish(
            Message(
                msgpack.packb({'order_id': order_id}),
                content_type='text/plain',
            ),
            'orders'
        )

    return ORJSONResponse({'status': 'success'})


def _prepare_response(data: Dict[str, Any]) -> ORJSONResponse:
    return ORJSONResponse(
        {
            'data': data,
        }
    )