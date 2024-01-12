from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from webapp.api.auth.router import auth_router
from webapp.api.category.router import category_router
from webapp.api.task.router import task_router
from webapp.db.metrics.metrics import metrics
from webapp.db.metrics.middleware import prometheus_metrics
from webapp.on_startup.redis import start_redis


def setup_middleware(app: FastAPI) -> None:
    # CORS Middleware should be the last.
    # See https://github.com/tiangolo/fastapi/issues/1663 .
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.middleware("http")(prometheus_metrics)


def setup_routers(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(task_router)
    app.include_router(category_router)
    app.add_route("/metrics", metrics)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print("START APP")
    yield
    print("END APP")


def create_app() -> FastAPI:
    app = FastAPI(docs_url="/swagger", lifespan=lifespan)

    setup_middleware(app)
    setup_routers(app)
    start_redis()

    return app
