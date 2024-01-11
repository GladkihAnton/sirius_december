import asyncio
from asyncio import AbstractEventLoop
from typing import AsyncGenerator

import pytest
from fastapi import FastAPI

from webapp.db.postgres import engine
from webapp.models import meta
from webapp.on_startup.main import create_app


@pytest.fixture(scope="session")
async def app(_migrate_db: None) -> FastAPI:
    return create_app()


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def _migrate_db() -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(meta.metadata.create_all)

    yield

    async with engine.begin() as conn:
        # to run pytest in web container
        await conn.run_sync(meta.metadata.create_all)
        # await conn.run_sync(meta.metadata.drop_all)
