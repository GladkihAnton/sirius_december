import asyncio

import pytest
from fastapi import FastAPI
import pytest_asyncio
from webapp.db.postgres import engine
from webapp.main import create_app
from webapp.models import meta


@pytest_asyncio.fixture(scope="session")
async def app(_migrate_db) -> FastAPI:
    return create_app()


@pytest_asyncio.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest_asyncio.fixture(scope="session")
async def _migrate_db():
    async with engine.begin() as conn:
        await conn.run_sync(meta.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(meta.metadata.drop_all)