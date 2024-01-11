import asyncio

import pytest
from fastapi import FastAPI

from tests.my_types import FixtureFunctionT

from webapp.db.postgres import engine
from webapp.main import create_app
from webapp.models import meta
from webapp.on_startup.redis import start_redis


@pytest.fixture(scope="session")
async def app(_migrate_db: FixtureFunctionT) -> FastAPI:
    await start_redis()

    return create_app()


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def _migrate_db() -> FixtureFunctionT:
    async with engine.begin() as conn:
        await conn.run_sync(meta.metadata.create_all)

    yield

    return
