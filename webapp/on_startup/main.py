from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from webapp.api.crud.activity.router import activity_router
from webapp.api.crud.router import crud_router
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
    app.include_router(crud_router)
    app.include_router(activity_router)


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger')
    start_redis()
    setup_middleware(app)
    setup_routers(app)

    return app
