from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from app.schemas.schema import UserInfo, UserEntity
from loguru import logger
from typing import Optional
from sqlalchemy import select
from app.services.security import hash_password, verify_password

async def create_user(session: AsyncSession, user_info: UserInfo) -> Optional[User]:
    """
    Создает нового пользователя в базе данных.

    Args:
        session (AsyncSession): Сессия базы данных.
        user_info (UserInfo): Информация о новом пользователе.

    Returns:
        Optional[User]: Созданный пользователь или None в случае ошибки.

    Raises:
        Exception: Если произошла ошибка при создании пользователя.
    """
    try:
        user_obj = User(**user_info.model_dump())
        session.add(user_obj)
        await session.commit()
        return user_obj
    except Exception as e:
        logger.error(f"Произошла ошибка при создании пользователя: {e}")
        await session.rollback()
        return None

async def get_user(session: AsyncSession, user_info: UserEntity) -> Optional[User]:
    """
    Получает пользователя по идентификатору.

    Args:
        session (AsyncSession): Сессия базы данных.
        user_info (UserEntity): Информация о пользователе.

    Returns:
        Optional[User]: Объект пользователя или None, если пользователь не найден.
    """
    try:
        user = (
            await session.scalars(
                select(User).where(
                    User.username == user_info.username,
                )
            )
        ).one_or_none()
        if user and verify_password(user_info.password, user.hashed_password):
            return user
        return None
    except Exception as e:
        logger.error(f"Произошла ошибка при получении пользователя: {e}")
        return None
