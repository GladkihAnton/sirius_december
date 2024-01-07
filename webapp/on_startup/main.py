from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from webapp.api.auth.router import auth_router
from webapp.api.crud.activity.router import activity_router
from webapp.api.crud.reservation.router import reservation_router
from webapp.api.crud.review.router import review_router
from webapp.api.crud.tour.router import tour_router
from webapp.api.crud.user.router import user_router
from webapp.integrations.metrics.metrics import metrics
from webapp.integrations.metrics.middleware import prometheus_metrics
from webapp.on_startup.redis import start_redis


def setup_middleware(app: FastAPI) -> None:
    # CORS Middleware should be the last.
    # See https://github.com/tiangolo/fastapi/issues/1663.
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
        activity_router,
        reservation_router,
        review_router,
        tour_router,
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
