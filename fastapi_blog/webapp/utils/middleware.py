import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from webapp.metrics import DEPS_LATENCY


class MeasureLatencyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        endpoint = request.url.path
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        DEPS_LATENCY.labels(endpoint=endpoint).observe(process_time)

        return response
