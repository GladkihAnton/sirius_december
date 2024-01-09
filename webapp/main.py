from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from webapp.api.group.router import group_router
from webapp.api.institution.router import institution_router
from webapp.api.journal.router import journal_router
from webapp.api.login.router import auth_router
from webapp.api.student.router import student_router
from webapp.api.subject.router import subject_router
from webapp.api.teacher.router import teacher_router
from webapp.api.group_subject.router import group_subject_router


def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*']
    )


def setup_routers(app: FastAPI) -> None:
    routers = [
        auth_router,
        group_router,
        institution_router,
        journal_router,
        student_router,
        subject_router,
        teacher_router,
        group_subject_router,
    ]

    for router in routers:
        app.include_router(router)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # await setup_redis()
    print('START APP')
    yield
    print('STOP APP')


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)

    setup_middleware(app)
    setup_routers(app)

    return app
