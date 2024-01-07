# работа с middleware
# middleware (промежуточное ПО) для измерения времени выполнения запроса к серверу
# компонент, который обрабатывает запросы и ответы между клиентом и сервером. Он может выполнять различные функции, такие как аутентификация, обработка ошибок, кэширование

import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from webapp.metrics import DEPS_LATENCY

# Измеряет время выполнения запроса и записывает его в метрику DEPS_LATENCY. Метрика DEPS_LATENCY используется для отслеживания времени выполнения запросов к зависимым сервисам (например, базе данных или API другого сервиса)
class MeasureLatencyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        endpoint = request.url.path
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        DEPS_LATENCY.labels(endpoint=endpoint).observe(process_time)

        return response
    
# отслеживаем производительность приложения
