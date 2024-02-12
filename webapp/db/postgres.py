from typing import AsyncGenerator

from sqlalchemy import QueuePool
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from conf.config import settings


def create_engine() -> AsyncEngine:
    return create_async_engine(
        settings.DB_URL,
        poolclass=QueuePool,
        connect_args={
            'statement_cache_size': 0,
        },
        pool_size=5,
        max_overflow=20,
        pool_recycle=3600,
    )


def create_session(engine: AsyncEngine | None = None) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine or create_engine(),
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )


engine = create_engine()
async_session = create_session(engine)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
