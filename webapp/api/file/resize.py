import uuid

import msgpack
from fastapi import Depends
from fastapi.responses import ORJSONResponse

from conf.config import settings
from webapp.api.file.router import file_router
from webapp.db import kafka
from webapp.schema.file.resize import ImageResize, ImageResizeResponse, ResizeStatusEnum
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@file_router.post('/resize', response_model=ImageResizeResponse)
async def resize(
    body: ImageResize = Depends(),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    producer = kafka.get_producer()

    task_id = uuid.uuid4().hex

    value = msgpack.packb(
        {
            'image': await body.image.read(),
            'task_id': task_id,
            'width': body.width,
            'height': body.height,
        }
    )

    await producer.send_and_wait(
        topic=settings.KAFKA_TOPIC,
        value=value,
        partition=kafka.get_partition(),
    )

    return ORJSONResponse(
        {
            'status': ResizeStatusEnum.status,
            'task_id': task_id,
        }
    )
