import os

import prometheus_client
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, CollectorRegistry, generate_latest
from prometheus_client.multiprocess import MultiProcessCollector
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


DEPS_LATENCY = prometheus_client.Histogram(
    'sirius_deps_latency_seconds',
    '',
    ['endpoint'],
    buckets=DEFAULT_BUCKETS,
)


def metrics(request: Request) -> Response:
    if 'prometheus_multiproc_dir' in os.environ:
        registry = CollectorRegistry()
        MultiProcessCollector(registry)
    else:
        registry = REGISTRY

    return Response(
        generate_latest(registry),
        headers={'Content-Type': CONTENT_TYPE_LATEST},
    )
