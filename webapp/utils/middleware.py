import time

from prometheus_client import Counter
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from webapp.metrics import DEPS_LATENCY

# Создаем счетчик для отслеживания запросов
REQUESTS_COUNTER = Counter(
    'sirius_api_requests_total',
    'Total number of requests to the API',
    ['method', 'endpoint', 'http_status'],
)

# Счетчики для успешных и неуспешных запросов
SUCCESSFUL_REQUESTS_COUNTER = Counter(
    'sirius_api_successful_requests_total',
    'Total number of successful requests to the API',
    ['method', 'endpoint', 'http_status']
)

UNSUCCESSFUL_REQUESTS_COUNTER = Counter(
    'sirius_api_unsuccessful_requests_total',
    'Total number of unsuccessful requests to the API',
    ['method', 'endpoint', 'http_status']
)


class MeasureLatencyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        endpoint = request.url.path
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        DEPS_LATENCY.labels(endpoint=endpoint).observe(process_time)

        # Увеличиваем счетчик запросов
        REQUESTS_COUNTER.labels(
            method=request.method,
            endpoint=endpoint,
            http_status=response.status_code,
        ).inc()

        # Увеличиваем счетчик успешных или неуспешных запросов
        if 200 <= response.status_code < 400:
            SUCCESSFUL_REQUESTS_COUNTER.labels(
                method=request.method,
                endpoint=endpoint,
                http_status=response.status_code
            ).inc()
        else:
            UNSUCCESSFUL_REQUESTS_COUNTER.labels(
                method=request.method,
                endpoint=endpoint,
                http_status=response.status_code
            ).inc()

        return response
