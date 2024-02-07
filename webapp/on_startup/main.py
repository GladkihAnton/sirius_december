from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from webapp.api.auth.router import auth_router
from webapp.api.crud.client.router import client_router
from webapp.api.crud.deal.router import deal_router
from webapp.api.crud.user.router import user_router
from webapp.integrations.metrics.metrics import metrics
from webapp.integrations.metrics.middleware import prometheus_metrics
from webapp.on_startup.redis import start_redis


def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.middleware('http')(prometheus_metrics)


def setup_routers(app: FastAPI) -> None:
    app.add_route('/metrics', metrics)
    routers = [
        auth_router,
        deal_router,
        client_router,
        user_router,
    ]
    for router in routers:
        app.include_router(router)


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger')
    start_redis()
    setup_middleware(app)
    setup_routers(app)

    return app
