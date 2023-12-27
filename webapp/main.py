from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from webapp.api.login.router import auth_router


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


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger')

    setup_middleware(app)
    setup_routers(app)

    return app
