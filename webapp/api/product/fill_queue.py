import io
import time
import uuid

import asyncpg
import msgpack
from aio_pika import Message, connect_robust
from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from conf.config import settings
from webapp.api.product.router import product_router
from webapp.db import kafka
from webapp.db.postgres import get_session
from webapp.db.rabbitmq import get_exchange_users, get_channel
from webapp.metrics import DEPS_LATENCY
from webapp.models.meta import DEFAULT_SCHEMA
from webapp.models.sirius.product import Product
from webapp.schema.file.resize import ImageResize, ImageResizeResponse, ResizeStatusEnum, FillQueue
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@product_router.post('/fill_queue')
async def fill_queue(
    body: FillQueue = Depends(),
    session: AsyncSession = Depends(get_session),
    # access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    # connection = await connect_robust(
    #     "amqp://rmuser:rmpassword@rabbitmq/",
    # )
    #
    # # Creating channel
    # channel = await connection.channel()
    #
    # # Declaring exchange
    # exchange = await channel.declare_exchange('direct', auto_delete=False, durable=True, passive=True)
    #
    # # Declaring queue
    # queue = await channel.declare_queue(f'users_product.0', auto_delete=False, durable=True, passive=True)
    #
    # # Binding queue
    # await queue.bind(exchange, f'users_product.0')
    exchange_users = get_exchange_users()
    channel = get_channel()


    # # Receiving message
    queue = await channel.declare_queue(f'test1', auto_delete=False, durable=True, passive=True)
    queue1 = await channel.declare_queue(f'test2', auto_delete=False, durable=True, passive=True)

    # body = msgpack.unpackb((await queue.get(timeout=5)).body)
    # body1 = msgpack.unpackb((await queue1.get(timeout=5)).body)
    # print(f'{body=}___{body1=}')

    # print(incoming_message.body.decode())
    # incoming_message = await queue1.get(timeout=5)
    # print(incoming_message.body.decode())
    # incoming_message = await queue2.get(timeout=5)
    # print(incoming_message.body.decode())
    #
    # # Confirm message
    # await incoming_message.ack()
    #
    # await queue.unbind(exchange, routing_key)
    # await queue.delete()
    # await connection.close()

    products = await session.stream_scalars(select(Product))
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
