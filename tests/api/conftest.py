import json
from pathlib import Path
from typing import AsyncGenerator, List
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from datetime import time, datetime
from webapp.db.postgres import engine, get_session
from webapp.models.meta import metadata


@pytest_asyncio.fixture()
async def client(app: FastAPI):
    async with AsyncClient(app=app, base_url='http://test.com') as client:
        yield client


@pytest_asyncio.fixture()
async def db_session(app: FastAPI) -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as connection:
        session_maker = async_sessionmaker(bind=connection)
        session = session_maker()

        async def mocked_session() -> AsyncGenerator[AsyncSession, None]:
            yield session

        app.dependency_overrides[get_session] = mocked_session

        yield session

        await connection.rollback()



@pytest_asyncio.fixture()
async def _load_fixtures(db_session: AsyncSession, fixtures: List[Path]):
    for fixture in fixtures:
        model = metadata.tables[fixture.stem]

        with open(fixture, 'r') as file:
            values = json.load(file)
        if fixture.stem == 'clinic.service':
            for data in values:
                data['duration'] = time(*map(int, data['duration'].split(':')))
        elif fixture.stem == 'clinic.timetable':
            for data in values:
                data['start'] = datetime.strptime(data['start'], "%Y-%m-%d %H:%M:%S%z")
                data['end'] = datetime.strptime(data['end'], "%Y-%m-%d %H:%M:%S%z")
        await db_session.execute(insert(model).values(values))  
        await db_session.commit()

    return

@pytest_asyncio.fixture()
async def _common_api_fixture(
    _load_fixtures,
) -> None:
    return
