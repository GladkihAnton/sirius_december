import asyncio
from asyncio import AbstractEventLoop

import pytest
from fastapi import FastAPI

from webapp.db.postgres import engine
from webapp.main import create_app
from webapp.models import meta
from webapp.on_startup.redis import start_redis


@pytest.fixture(scope='session')
async def app(_migrate_db: None) -> FastAPI:
    await start_redis()

    return create_app()


@pytest.fixture(scope='session')
def event_loop() -> AbstractEventLoop:
    return asyncio.get_event_loop()


@pytest.fixture(scope='session')
async def _migrate_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(meta.metadata.create_all)

    return

    # async with engine.begin() as conn:
    #     await conn.run_sync(meta.metadata.drop_all)
