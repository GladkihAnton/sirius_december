from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.api.log_route import LogRoute
from app.db import crud, session
from app.schemas.schema import UserInfo, UserResponse, UserEntity
from app.core.exceptions import UserNotFoundException

router = APIRouter(route_class=LogRoute)

from fastapi import HTTPException

@router.post(
    path="/сreate", 
    response_model=UserInfo,
    status_code=status.HTTP_201_CREATED
)
async def create_user(user_info: UserInfo, db: AsyncSession = Depends(session.get_db)):
    """
    Создание нового пользователя.

    Args:
        user_info (UserInfo): Информация о новом пользователе.
        db (Session): Сессия базы данных.

    Returns:
        UserInfo: Созданный пользователь.

    Raises:
        HTTPException: Если произошла ошибка при создании пользователя.
    """
    try:
        created_user = await crud.create_user(db, user_info)

        if created_user is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )

        return created_user
    except Exception as e:
        logger.error(f"Произошла ошибка во время создания пользователя: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )



@router.post(
    "/get",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
async def get_user(user_info: UserEntity, db: AsyncSession = Depends(session.get_db)):
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
            # Помечаем пользовательское исключение для обработки внутри трай-эксепт
            raise UserNotFoundException()

        return UserResponse(username=user.username)
    except UserNotFoundException:
        # Здесь вы можете вернуть пользователю информацию о том, что пользователь не найден
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except Exception as e:
        logger.error(f"Произошла ошибка во время получения пользователя: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )