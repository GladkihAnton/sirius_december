from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.log_route import LogRoute
from app.core.exceptions import UserNotFoundException
from app.db import crud, session
from app.schemas.schema import UserEntity, UserInfo, UserResponse

router = APIRouter(route_class=LogRoute)


@router.post(path="/сreate", response_model=UserInfo, status_code=status.HTTP_201_CREATED)
async def create_user(user_info: UserInfo, db: AsyncSession = Depends(session.get_db)) -> UserInfo:
    """
    Создание нового пользователя.

    Args:
        user_info (UserInfo): Информация о новом пользователе.
        db (AsyncSession): Сессия базы данных.

    Returns:
        UserInfo: Созданный пользователь.

    Raises:
        HTTPException: Если произошла ошибка при создании пользователя.
    """
    try:
        created_user = await crud.create_user(db, user_info)

        if created_user is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")

        return created_user
    except Exception as e:
        logger.error(f"Произошла ошибка во время создания пользователя: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.post("/get", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_info: UserEntity, db: AsyncSession = Depends(session.get_db)) -> UserResponse:
    """
    Получение пользователя по информации о пользователе.

    Args:
        user_info (UserEntity): Информация о пользователе (имя пользователя и пароль).
        db (AsyncSession): Сессия базы данных.

    Returns:
        UserResponse: Информация о пользователе.

    Raises:
        HTTPException: Если пользователь не найден.
    """
    try:
        user = await crud.get_user(db, user_info)

        if user is None:
            raise UserNotFoundException()

        return UserResponse(username=user.username)
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        logger.error(f"Произошла ошибка во время получения пользователя: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
