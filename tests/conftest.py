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
    fixtures = ['fixture/sirius/sirius.user.json',
                'fixture/sirius/sirius.post.json',
                'fixture/sirius/sirius.comment.json',]
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


# В данном коде определяются несколько фикстур для тестирования FastAPI-приложения,
# использующего базу данных Postgres.

# Фикстура app создает экземпляр FastAPI-приложения, используя функцию create_app() из
# модуля webapp.main. Перед созданием приложения выполняется фикстура _migrate_db,
# которая создает все необходимые таблицы в базе данных. После выполнения тестов
# фикстура _migrate_db удаляет все таблицы из базы данных.

# Фикстура event_loop возвращает экземпляр цикла событий asyncio, который
# используется для асинхронной обработки запросов в приложении.

# Фикстура _migrate_db создает и удаляет таблицы в базе данных Postgres.
# Она используется в фикстуре app для создания приложения с уже
# существующими таблицами в базе данных.

# В целом, данный код предназначен для подготовки окружения для тестирования
# FastAPI-приложения с использованием базы данных Postgres. Он позволяет
# создавать и удалять таблицы в базе данных перед и после выполнения тестов,
# а также создавать экземпляр приложения для тестирования его функциональности.