import time
import asyncio
from functools import wraps

from webapp.utils.middleware import INTEGRATION_METHOD_LATENCY


def measure_integration_latency(method_name, integration_point):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()

            # Проверяем, является ли функция асинхронной
            # и вызываем её соответствующим образом
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            process_time = time.time() - start_time
            INTEGRATION_METHOD_LATENCY.labels(
                method=method_name, integration_point=integration_point
            ).observe(process_time)

            return result

        return wrapper

    return decorator
