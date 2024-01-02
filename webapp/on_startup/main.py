from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from webapp.api.crud.activity.router import activity_router
from webapp.api.crud.reservation.router import reservation_router
from webapp.api.crud.review.router import review_router
from webapp.api.crud.tour.router import tour_router
from webapp.api.crud.user.router import user_router
from webapp.api.login.router import auth_router
from webapp.on_startup.redis import start_redis


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
    app.include_router(activity_router)
    app.include_router(reservation_router)
    app.include_router(review_router)
    app.include_router(tour_router)
    app.include_router(user_router)


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger')
    start_redis()
    setup_middleware(app)
    setup_routers(app)

    return app
