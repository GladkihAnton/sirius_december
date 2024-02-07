from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from webapp.api.employee.router import employee_router
from webapp.api.login.router import auth_router
from webapp.api.vacation.router import vacation_router
from webapp.metrics import metrics
from webapp.on_shutdown import stop_producer
from webapp.on_startup.kafka import create_producer
from webapp.on_startup.redis import start_redis
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
    app.include_router(employee_router)
    app.include_router(vacation_router)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await start_redis()
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
