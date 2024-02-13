from asyncio import QueueEmpty
from typing import Any, Dict

import msgpack
from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.product.router import product_router
from webapp.cache.rabbit_key_builder import get_user_products_queue_key
from webapp.db.postgres import get_session
from webapp.db.rabbitmq import get_exchange_users, get_channel
from webapp.models.sirius.product import Product
from webapp.schema.product.base import ProductModel
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@product_router.post('/get_random_product')
async def get_random_product(
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    exchange_users = get_exchange_users()
    channel = get_channel()

    queue_key = get_user_products_queue_key(access_token['user_id'])

    queue = await channel.declare_queue(queue_key, auto_delete=False, durable=True, passive=True)

    try:
        body = (await queue.get(timeout=3, no_ack=False)).body # TODO TEMP
    except QueueEmpty:
        return _prepare_response({})

    product_id = msgpack.unpackb(body)['product_id']

    product = (await session.scalars(select(Product).where(Product.id == product_id))).one()

    return _prepare_response(ProductModel.model_validate(product).model_dump(mode='json'))

def _prepare_response(data: Dict[str, Any]) -> ORJSONResponse:
    return ORJSONResponse(
        {
            'data': data,
        }
    )