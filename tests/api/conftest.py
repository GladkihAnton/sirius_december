# conftest
import json
import uuid
from pathlib import Path
from typing import AsyncGenerator, List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tests.const import URLS
from tests.mocking.kafka import TestKafkaProducer
from tests.my_types import FixtureFunctionT

from webapp.db import kafka
from webapp.db.postgres import engine, get_session
from webapp.models.meta import metadata


TEST_USERNAME = 'autotest'
TEST_PASSWORD = 'qwerty'


@pytest.fixture()
def username() -> str:
    return TEST_USERNAME


@pytest.fixture()
def password() -> str:
    return TEST_PASSWORD


@pytest.fixture()
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test.com') as client:
        yield client


@pytest.fixture()
async def db_session(app: FastAPI) -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as connection:
        session_maker = async_sessionmaker(bind=connection)
        session = session_maker()

        async def mocked_session() -> AsyncGenerator[AsyncSession, None]:
            yield session

        app.dependency_overrides[get_session] = mocked_session  # noqa

        yield session

        await connection.rollback()


@pytest.fixture()
async def _load_fixtures(db_session: AsyncSession, fixtures: List[Path]) -> None:
    for fixture in fixtures:
        model = metadata.tables[fixture.stem]

        with open(fixture, 'r') as file:
            values = json.load(file)

        await db_session.execute(insert(model).values(values))
        await db_session.commit()


@pytest.fixture()
def _mock_kafka(monkeypatch: pytest.MonkeyPatch, kafka_received_messages: List, mocked_hex: str) -> None:
    monkeypatch.setattr(kafka, 'get_producer', lambda: TestKafkaProducer(kafka_received_messages))
    monkeypatch.setattr(kafka, 'get_partition', lambda: 1)
    monkeypatch.setattr(uuid.UUID, 'hex', mocked_hex)


@pytest.fixture()
def kafka_received_messages() -> List:
    return []


@pytest.fixture()
async def access_token(
    client: AsyncClient,
    username: str,
    password: str,
) -> str:
    response = await client.post(URLS['auth']['login'], json={'username': username, 'password': password})
    return response.json()['access_token']


@pytest.fixture()
async def _common_api_fixture(
    _load_fixtures: FixtureFunctionT,
) -> None:
    return


@pytest.fixture()
async def _common_api_with_kafka_fixture(
    _common_api_fixture: FixtureFunctionT,
    _mock_kafka: FixtureFunctionT,
) -> None:
    return


# Этот код определяет фикстуры для тестирования API.

# Сначала импортируются необходимые модули и объекты,
# такие как FastAPI, AsyncClient, AsyncSession, и т.д.

# Затем определяются фикстуры для клиента API (client), сессии базы данных (db_session),
# загрузки фикстур в базу данных (_load_fixtures), мокирования Kafka (_mock_kafka),
# списка полученных сообщений Kafka (kafka_received_messages) и токена доступа (access_token).

# Каждая фикстура выполняет определенные задачи, такие как подключение к базе данных,
# создание клиента API, загрузка фикстур в базу данных, мокирование Kafka и т.д.

# Наконец, определяются две фикстуры _common_api_fixture и _common_api_with_kafka_fixture,
# которые используют другие фикстуры для создания общего набора фикстур для тестирования API.
# Эти фикстуры могут использоваться в других тестах для обеспечения общих условий.