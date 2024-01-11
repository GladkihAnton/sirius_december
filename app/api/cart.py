import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.log_route import LogRoute
from app.core.exceptions import UserNotFoundException
from app.db import crud, session
from app.schemas.schema import OrderInfo, ProductInfo, UserEntity, UserResponse
from app.cache.cache import redis_set, redis_get, redis_drop_key

router = APIRouter(route_class=LogRoute)


@router.post("/add_to_cart", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def add_to_cart(
    user_info: UserEntity, product_info: ProductInfo, quantity: int, db: AsyncSession = Depends(session.get_db)
) -> UserResponse:
    """
    Добавление продукта в корзину пользователя.

    Args:
        user_info (UserEntity): Информация о пользователе (имя пользователя и пароль).
        product_info (ProductInfo): Информация о продукте.
        quantity (int): Количество продукта для добавления в корзину.
        db (AsyncSession): Сессия базы данных.

    Returns:
        UserResponse: Информация о пользователе с обновленной корзиной.

    Raises:
        HTTPException: Если пользователь не найден или произошла ошибка при добавлении продукта в корзину.
    """
    try:
        user = await crud.get_user(db, user_info)

        if user is None:
            raise UserNotFoundException()

        order = await crud.add_product_to_cart(db, user, product_info, quantity)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add product to cart"
            )
        await redis_drop_key("order", str(user.id))
        serialized = UserResponse(
            username=user.username, orders=[
                OrderInfo(user_id=str(order.user_id), status=order.status)
            ]
        )
        return ORJSONResponse(
            UserResponse.model_validate(
                serialized
            ).model_dump()
        )
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        logger.error(
            f"An error occurred while adding a product to the cart: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.post("/place_order", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def place_order(user_info: UserEntity, db: AsyncSession = Depends(session.get_db)) -> UserResponse:
    """
    Оформление заказа на основе корзины пользователя.

    Args:
        user_info (UserEntity): Информация о пользователе (имя пользователя и пароль).
        db (AsyncSession): Сессия базы данных.

    Returns:
        UserResponse: Информация о пользователе с обновленным заказом.

    Raises:
        HTTPException: Если пользователь не найден или произошла ошибка при оформлении заказа.
    """
    try:
        user = await crud.get_user(db, user_info)

        if user is None:
            raise UserNotFoundException()

        order = await crud.place_order(db, user)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to place order")
        await redis_drop_key("order", str(user.id))
        serialized = UserResponse(
            username=user.username, orders=[
                OrderInfo(user_id=str(order.user_id), status=order.status)
            ]
        )
        return ORJSONResponse(
            UserResponse.model_validate(
                serialized
            ).model_dump()
        )
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        logger.error(f"An error occurred while placing an order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.put("/update_cart_product/{product_id}", response_model=OrderInfo, status_code=status.HTTP_200_OK)
async def update_cart_product(product_id: uuid.UUID, quantity: int, db: AsyncSession = Depends(session.get_db)) -> OrderInfo:
    """
    Обновление количества продукта в корзине.

    Args:
        product_id (uuid.UUID): Идентификатор продукта в корзине, который нужно обновить.
        quantity (int): Новое количество продукта.
        db (AsyncSession): Сессия базы данных.

    Returns:
        OrderInfo: Обновленная корзина пользователя.

    Raises:
        HTTPException: Если произошла ошибка при обновлении продукта в корзине.
    """
    try:
        updated_order = await crud.update_cart_product(db, product_id, quantity)

        if updated_order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found in the cart"
            )
        await redis_drop_key("order", str(updated_order.user_id))
        serialized = OrderInfo(user_id=str(
            updated_order.user_id), status=updated_order.status)
        return ORJSONResponse(
            OrderInfo.model_validate(serialized).model_dump()
        )
    except Exception as e:
        logger.error(
            f"Произошла ошибка во время обновления продукта в корзине: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.delete("/remove_from_cart/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(session.get_db),
) -> None:
    """
    Удаление продукта из корзины.

    Args:
        product_id (uuid.UUID): Идентификатор продукта в корзине, который нужно удалить.
        db (AsyncSession): Сессия базы данных.

    Raises:
        HTTPException: Если произошла ошибка при удалении продукта из корзины.
    """
    try:
        result = await crud.remove_from_cart(db, str(product_id))

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found in the cart"
            )
    except Exception as e:
        logger.error(
            f"Произошла ошибка во время удаления продукта из корзины: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/get_cart/{order_id}", response_model=OrderInfo, status_code=status.HTTP_200_OK)
async def get_cart(order_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession = Depends(session.get_db)) -> OrderInfo:
    """
    Получение информации о корзине пользователя.

    Args:
        order_id (uuid.UUID): Идентификатор заказа (корзины).
        db (AsyncSession): Сессия базы данных.
        user_id (uuid.UUID): Идентификатор пользователя.

    Returns:
        OrderInfo: Информация о корзине пользователя.

    Raises:
        HTTPException: Если произошла ошибка при получении информации о корзине.
    """
    try:
        order_info = await redis_get("order", str(user_id))

        if order_info:
            return ORJSONResponse(order_info)

        order_info = await crud.get_cart(db, order_id, user_id)

        if order_info is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Cart with id {order_id} not found")
        serialized = {
            "user_id": str(order_info.user_id),
            "status": order_info.status,
            "id": str(order_id)
        }
        await redis_set("order", str(order_info.user_id), serialized)
        return ORJSONResponse(serialized)
    except Exception as e:
        logger.error(f"An error occurred while getting cart information: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
