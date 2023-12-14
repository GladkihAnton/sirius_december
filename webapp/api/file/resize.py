import uuid

import msgpack
from fastapi import Depends
from fastapi.responses import ORJSONResponse

from conf.config import settings
from webapp.api.file.router import file_router
from webapp.db.kafka import get_partition, get_producer
from webapp.schema.file.resize import ImageResize, ImageResizeResponse, ResizeStatusEnum


@file_router.post('/resize', response_model=ImageResizeResponse)
async def resize(
    body: ImageResize = Depends(),
) -> ORJSONResponse:
    producer = get_producer()

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
        partition=get_partition(),
    )

    return ORJSONResponse(
        {
            'status': ResizeStatusEnum.status,
            'task_id': task_id,
        }
    )
