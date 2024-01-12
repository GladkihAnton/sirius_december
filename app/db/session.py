from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import Config

# Создаем асинхронный движок SQLAlchemy и устанавливаем соединение с базой данных
engine = create_async_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=False, future=True)


# Создаем асинхронную фабрику сессий
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Создает и предоставляет сессию базы данных как асинхронный контекстный ресурс.

    Yields:
        sqlalchemy.ext.asyncio.AsyncSession: Сессия базы данных, предоставляемая как асинхронный контекстный ресурс.

    Notes:
        Эта функция создает новую сессию базы данных с использованием асинхронной фабрики сессий AsyncSessionLocal,
        предоставляет ее как асинхронный контекстный ресурс с помощью yield, и автоматически закрывает сессию после завершения
        блока контекста (в блоке `finally`). Это гарантирует корректное управление сессией и предотвращение
        утечек ресурсов.
    """
    async with AsyncSessionLocal() as session:
        yield session
