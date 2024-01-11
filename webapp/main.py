from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from webapp.api.crud.order.router import order_router
from webapp.api.crud.order_product.router import op_router
from webapp.api.crud.product.router import product_router
from webapp.api.crud.restaurant.router import restaurant_router
from webapp.api.crud.user.router import user_router
from webapp.api.login.router import auth_router
from webapp.api.v1.router import v1_router
from webapp.db.redis import start_redis
from webapp.integrations.metrics.metrics import metrics
from webapp.integrations.metrics.middleware import prometheus_metrics


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
    app.middleware('http')(prometheus_metrics)


def setup_routers(app: FastAPI) -> None:
    app.add_route('/metrics', metrics)
    routers = [
        auth_router,
        product_router,
        restaurant_router,
        order_router,
        op_router,
        user_router,
        v1_router,
    ]
    for router in routers:
        app.include_router(router)


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger')
    start_redis()
    setup_middleware(app)
    setup_routers(app)

    return app
