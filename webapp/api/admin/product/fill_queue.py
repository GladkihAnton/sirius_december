import msgpack
from aio_pika import Message
from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.admin.product.router import product_router
from webapp.db.postgres import get_session
from webapp.db.rabbitmq import get_exchange_users
from webapp.models.sirius.product import Product
from webapp.schema.file.resize import FillQueue


@product_router.post('/fill_queue')
async def fill_queue(
    body: FillQueue = Depends(),
    session: AsyncSession = Depends(get_session),
    # access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    exchange_users = get_exchange_users()

    products = await session.stream_scalars(select(Product).order_by(func.random()))
    async for product in products:
        await exchange_users.publish(
            Message(
                msgpack.packb({'product_id': product.id}),
                content_type='text/plain',
                headers={'foo': 'bar'}
            ),
            ''
        )


    return ORJSONResponse(
        {
            'status': 'success',
        }
    )
