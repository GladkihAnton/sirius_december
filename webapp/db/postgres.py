from sqlalchemy import NullPool, QueuePool
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from conf.config import settings


settings.DB_URL
def create_engine() -> AsyncEngine:
    return create_async_engine(
        'postgresql+asyncpg://postgres1:postgres1@web_db:5432/main_db',
        poolclass=QueuePool,
        connect_args={
            'statement_cache_size': 0,
        },
    )


def create_session(engine: AsyncEngine | None = None) -> async_sessionmaker:
    return async_sessionmaker(
        bind=engine or create_engine(),
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )


engine = create_engine()
async_session = create_session(engine)


async def get_session():
    async with async_session() as session:
        yield session
