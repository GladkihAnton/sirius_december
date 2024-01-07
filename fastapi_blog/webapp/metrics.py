# Здесь как раз определяется метрика DEPS_LATENCY, которая используется в middleware 
import os

import prometheus_client  # type: ignore
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, CollectorRegistry, generate_latest
from prometheus_client.multiprocess import MultiProcessCollector  # type: ignore
from starlette.requests import Request
from starlette.responses import Response

DEFAULT_BUCKETS = (
    0.005,
    0.01,
    0.025,
    0.05,
    0.075,
    0.1,
    0.125,
    0.15,
    0.175,
    0.2,
    0.25,
    0.3,
    0.5,
    0.75,
    1.0,
    2.5,
    5.0,
    7.5,
    float('+inf'),
)


# TODO in middleware
# prometheus_client.Counter(
#     'sirius_deps_latency_seconds',
#     '',
#     ['endpoint'],)

# histogram_quantile(0.99, sum(rate(sirius_deps_latency_seconds_bucket[1m])) by (le, endpoint))
# среднее время обработки за 1 мин
DEPS_LATENCY = prometheus_client.Histogram(
    'sirius_deps_latency_seconds',
    '',
    ['endpoint'],
    buckets=DEFAULT_BUCKETS,
)
# предоставляет метрики приложения в формате Prometheus
# использует библиотеку prometheus_client для регистрации метрик и генерации данных в формате Prometheus
#  вызывается, когда приложение получает запрос на /metrics. В ответ на этот запрос, функция возвращает данные метрик в формате Prometheus

def metrics(request: Request) -> Response:
    if 'prometheus_multiproc_dir' in os.environ:
        registry = CollectorRegistry()
        MultiProcessCollector(registry)
    else:
        registry = REGISTRY

    return Response(generate_latest(registry), headers={'Content-Type': CONTENT_TYPE_LATEST})
