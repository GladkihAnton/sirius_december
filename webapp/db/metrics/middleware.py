from time import monotonic
from typing import Any, Awaitable, Callable

from starlette.requests import Request

from webapp.db.metrics.metrics import (ERROR_COUNT, REQUEST_COUNT,
                                       ROUTES_LATENCY)


async def prometheus_metrics(
    request: Request, call_next: Callable[..., Awaitable[Any]]
) -> Awaitable[Any]:
    method = request.method
    path = request.url.path

    start_time = monotonic()
    response = await call_next(request)
    process_time = monotonic() - start_time
    if path in ["/favicon.ico", "/metrics"]:
        return response
    REQUEST_COUNT.labels(
        method=method, endpoint=path, http_status=str(response.status_code)
    ).inc()
    ROUTES_LATENCY.labels(method=method, endpoint=path).observe(process_time)

    if 400 <= response.status_code < 600:
        ERROR_COUNT.labels(
            method=method, endpoint=path, http_status=str(response.status_code)
        ).inc()

    return response
