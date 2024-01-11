from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from webapp.api.comment.router import comment_router
from webapp.api.login.router import auth_router
from webapp.api.post.router import post_router
from webapp.metrics import metrics
from webapp.on_shutdown import close_redis_pool, stop_producer
from webapp.on_startup.kafka import create_producer
from webapp.on_startup.redis import get_redis_pool
from webapp.utils.middleware import MeasureLatencyMiddleware


def setup_middleware(app: FastAPI) -> None:
    # CORS Middleware should be the last.
    # See https://github.com/tiangolo/fastapi/issues/1663 .
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.add_middleware(MeasureLatencyMiddleware)


def setup_routers(app: FastAPI) -> None:
    app.add_route('/metrics', metrics)

    app.include_router(auth_router)
    app.include_router(post_router)
    app.include_router(comment_router)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await create_producer()
    await get_redis_pool()
    print('START APP')
    yield
    await stop_producer()
    await close_redis_pool()
    print('END APP')


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)

    setup_middleware(app)
    setup_routers(app)

    return app