import json
import datetime
from pathlib import Path
from typing import AsyncGenerator, List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tests.const import URLS
from tests.mocking.redis import TestRedisClient
from tests.my_types import FixtureFunctionT

from webapp.db.postgres import engine, get_session
from webapp.db.redis import get_redis
from webapp.models.meta import metadata


@pytest.fixture()
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test.com") as client:
        yield client


@pytest.fixture()
async def db_session(app: FastAPI) -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as connection:
        session_maker = async_sessionmaker(bind=connection)
        session = session_maker(expire_on_commit=False)

        async def mocked_session() -> AsyncGenerator[AsyncSession, None]:
            yield session

        app.dependency_overrides[get_session] = mocked_session  # noqa

        yield session

        await connection.rollback()


@pytest.fixture()
async def _load_fixtures(db_session: AsyncSession, fixtures: List[Path]) -> FixtureFunctionT:
    for fixture in fixtures:
        model = metadata.tables[fixture.stem]

        with open(fixture, "r") as file:
            values = json.load(file)
        for value in values:
            if "date_time" in value:
                value["date_time"] = datetime.datetime.strptime(value["date_time"], "%Y-%m-%d %H:%M:%S %z")

        await db_session.execute(insert(model).values(values))
        await db_session.commit()

    return


@pytest.fixture()
async def access_token(
    client: AsyncClient,
    username: str,
    password: str,
) -> str:
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = await client.post(
        URLS["api"]["v1"]["auth"]["token"],
        data={"username": username, "password": password},
        headers=headers,
    )
    return response.json().get("access_token")


@pytest.fixture()
def _mock_redis(monkeypatch: pytest.MonkeyPatch) -> None:
    redis = get_redis()
    monkeypatch.setattr(redis, "set", TestRedisClient.set)
    monkeypatch.setattr(redis, "get", TestRedisClient.get)
    monkeypatch.setattr(redis, "delete", TestRedisClient.delete)


@pytest.fixture()
async def _common_api_fixture(
    _load_fixtures: FixtureFunctionT,
) -> None:
    return


@pytest.fixture()
async def _common_api_fixture_with_redis(_load_fixtures: FixtureFunctionT, _mock_redis: FixtureFunctionT) -> None:
    return
