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
    exchange_users = get_exchange_users()

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
