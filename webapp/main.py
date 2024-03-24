from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from webapp.api.admin.router import admin_router
from webapp.api.customer.router import customer_router
from webapp.api.delivery.router import delivery_router
from webapp.api.login.router import auth_router
from webapp.metrics import metrics
from webapp.middleware.logger import LogServerMiddleware
from webapp.on_shutdown import stop_producer
from webapp.on_startup.kafka import create_producer
from webapp.on_startup.logger import setup_logger
from webapp.on_startup.rabbit import start_rabbit
from webapp.on_startup.redis import start_redis


def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(
        LogServerMiddleware,
    )

    # CORS Middleware should be the last.
    # See https://github.com/tiangolo/fastapi/issues/1663 .
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def setup_routers(app: FastAPI) -> None:
    app.add_route('/metrics', metrics)

    app.include_router(auth_router)
    app.include_router(admin_router)
    app.include_router(customer_router)
    app.include_router(delivery_router)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    setup_logger()
    await start_redis()
    await start_rabbit()
    await create_producer()
    print('START APP')
    yield
    await stop_producer()
    print('END APP')


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)

    setup_middleware(app)
    setup_routers(app)

    return app
