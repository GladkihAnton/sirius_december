from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from conf.config import settings
from webapp.db.postgres import get_session


@pytest.fixture()
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test.com') as client:
        yield client


@pytest.fixture()
async def db_session(app: FastAPI) -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(settings.DB_URL)
    # connection = engine.connect()  # noqa
    # transaction = connection.begin()  # noqa

    session_maker = async_sessionmaker(bind=engine)

    async with session_maker() as session:

        async def mocked_session() -> AsyncGenerator[AsyncSession, None]:
            yield session

        app.dependency_overrides[get_session] = mocked_session  # noqa

        yield session
        await session.rollback()

    # await transaction.rollback()  # noqa
    # await connection.close()  # noqa
