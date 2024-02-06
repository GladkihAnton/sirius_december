import asyncio

import pytest
from fastapi import FastAPI

from scripts.load_data import main as load_data_main
from tests.my_types import FixtureFunctionT

from webapp.db.postgres import engine
from webapp.main import create_app
from webapp.models import meta


@pytest.fixture(scope='session', autouse=True)
def _run_after_tests():
    yield

    loop = asyncio.get_event_loop()
    fixtures = [
        'fixture/sirius/sirius.user.json',
        'fixture/sirius/sirius.course.json',
        'fixture/sirius/sirius.lesson.json',
        'fixture/sirius/sirius.file.json',
        'fixture/sirius/sirius.subscription.json',
    ]
    loop.run_until_complete(load_data_main(fixtures))


@pytest.fixture(scope='session')
async def app(_migrate_db: FixtureFunctionT) -> FastAPI:
    return create_app()


@pytest.fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='session')
async def _migrate_db() -> FixtureFunctionT:
    async with engine.begin() as conn:
        await conn.run_sync(meta.metadata.drop_all)
        await conn.run_sync(meta.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(meta.metadata.drop_all)
        await conn.run_sync(meta.metadata.create_all)
