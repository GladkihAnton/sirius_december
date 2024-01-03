from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from webapp.api.file.router import file_router
from webapp.api.login.router import auth_router
from webapp.api.chouse_restaurant.router import restaurants_router
from webapp.on_shutdown import stop_producer
from webapp.on_startup.kafka import create_producer


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


def setup_routers(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(file_router)
    app.include_router(restaurants_router)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
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
