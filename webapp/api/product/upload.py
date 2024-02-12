import io
import time
import uuid

import asyncpg
import msgpack
from fastapi import Depends
from fastapi.responses import ORJSONResponse

from conf.config import settings
from webapp.api.product.router import product_router
from webapp.db import kafka
from webapp.metrics import DEPS_LATENCY
from webapp.models.meta import DEFAULT_SCHEMA
from webapp.models.sirius.product import Product
from webapp.schema.file.resize import ImageResize, ImageResizeResponse, ResizeStatusEnum
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@product_router.post('/upload', response_model=ImageResizeResponse)
async def resize(
    body: ImageResize = Depends(),
    # access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    conn = await asyncpg.connect(
        host=settings.DB_HOST,
        user=settings.DB_USERNAME,
        password=settings.DB_PASSWORD,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    )

    buff = body.file.file
    buff.seek(0)

    columns = buff.readline().decode().strip().split(',')

    await conn.copy_to_table(
        'product', source=buff, schema_name=DEFAULT_SCHEMA,
        columns=columns, format='csv', header=False,
    )

    await conn.close()

    return ORJSONResponse(
        {
            'status': 'success'
        }
    )
