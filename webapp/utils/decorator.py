import json
import time
from datetime import datetime
from functools import wraps

from fastapi import status
from fastapi.responses import ORJSONResponse

from webapp.db import kafka
from webapp.metrics import DEPS_LATENCY


def kafka_producer_decorator(topic, status_code=status.HTTP_200_OK):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)

            if hasattr(result, 'dict'):
                result_data = result.dict()
            elif isinstance(result, dict):
                result_data = result
            else:
                return result

            for key, value in result_data.items():
                if isinstance(value, datetime):
                    result_data[key] = value.isoformat()

            processing_time = time.time() - start
            result_data['processing_time'] = processing_time

            await kafka.producer.send_and_wait(
                topic=topic,
                value=json.dumps(result_data).encode('utf-8'),
            )

            DEPS_LATENCY.labels(endpoint=topic).observe(time.time() - start)

            return ORJSONResponse(result_data, status_code=status_code)

        return wrapper

    return decorator
