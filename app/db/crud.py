import uuid
from typing import Optional, List

from loguru import logger
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Order, OrderProduct, Product, User
from app.schemas.schema import OrderInfo, ProductInfo, UserEntity, UserInfo
from app.services.security import verify_password


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

async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    return (
            await session.scalars(
                select(User).where(
                    User.username == username,
                )
            )
    ).one_or_none()


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


async def add_product_to_cart(
    session: AsyncSession, user: User, product_info: ProductInfo, quantity: int
) -> Optional[Order]:
    """
    Добавляет продукт в корзину пользователя.

    Args:
        session (AsyncSession): Сессия базы данных.
        user (User): Пользователь, в чью корзину добавляется продукт.
        product_info (ProductInfo): Информация о продукте.
        quantity (int): Количество продукта для добавления в корзину.

    Returns:
        Optional[Order]: Объект корзины пользователя или None в случае ошибки.

    Raises:
        Exception: Если произошла ошибка при добавлении продукта в корзину.
    """
    try:
        product = (
            await session.scalars(
                select(Product).where(
                    Product.name == product_info.name,
                )
            )
        ).one_or_none()

        if not product:
            logger.error(f"Продукт с именем {product_info.name} не найден.")
            return None

        order = (
            await session.scalars(
                select(Order).where(
                    Order.user_id == user.id,
                    Order.status == 'cart',
                )
            )
        ).one_or_none()

        if not order:
            order = Order(user_id=user.id, status='cart')
            session.add(order)
            await session.commit()

        order_product = OrderProduct(order_id=order.id, product_id=product.id, quantity=quantity)
        session.add(order_product)
        await session.commit()

        return order
    except Exception as e:
        logger.error(f"Произошла ошибка при добавлении продукта в корзину: {e}")
        await session.rollback()
        return None


async def place_order(session: AsyncSession, user: User) -> Optional[Order]:
    """
    Оформляет заказ на основе корзины пользователя.

    Args:
        session (AsyncSession): Сессия базы данных.
        user (User): Пользователь, для которого оформляется заказ.

    Returns:
        Optional[Order]: Объект заказа или None в случае ошибки.

    Raises:
        Exception: Если произошла ошибка при оформлении заказа.
    """
    try:
        order = (
            await session.scalars(
                select(Order).where(
                    Order.user_id == user.id,
                    Order.status == 'cart',
                )
            )
        ).one_or_none()

        if not order:
            logger.error(f"Корзина пользователя {user.username} пуста.")
            return None

        order.status = 'placed'
        await session.commit()

        return order
    except Exception as e:
        logger.error(f"Произошла ошибка при оформлении заказа: {e}")
        await session.rollback()
        return None


async def create_product(session: AsyncSession, product_info: ProductInfo) -> Optional[ProductInfo]:
    """
    Создает новый продукт в базе данных.

    Args:
        session (AsyncSession): Сессия базы данных.
        product_info (ProductInfo): Информация о новом продукте.

    Returns:
        Optional[Product]: Созданный продукт или None в случае ошибки.

    Raises:
        Exception: Если произошла ошибка при создании продукта.
    """
    try:
        product_obj = Product(**product_info.model_dump())
        session.add(product_obj)
        await session.commit()
        return ProductInfo(id=product_obj.id, name=product_obj.name, description=product_obj.description, price=product_obj.price)
    except Exception as e:
        logger.error(f"Произошла ошибка при создании продукта: {e}")
        await session.rollback()
        return None


async def update_product(session: AsyncSession, product_id: uuid.UUID, updated_info: ProductInfo) -> Optional[Product]:
    """
    Обновляет информацию о продукте.

    Args:
        session (AsyncSession): Сессия базы данных.
        product_id (uuid.UUID): Идентификатор продукта, который нужно обновить.
        updated_info (ProductInfo): Новая информация о продукте.

    Returns:
        Optional[Product]: Обновленный продукт или None в случае ошибки.

    Raises:
        Exception: Если произошла ошибка при обновлении продукта.
    """
    try:
        product = (await session.scalars(select(Product).where(Product.id == product_id))).one_or_none()

        if product:
            for key, value in updated_info.model_dump().items():
                setattr(product, key, value)

            await session.commit()
            return product
        else:
            logger.error(f"Продукт с id {product_id} не найден.")
            return None
    except Exception as e:
        logger.error(f"Произошла ошибка при обновлении продукта: {e}")
        await session.rollback()
        return None


async def delete_product(session: AsyncSession, product_id: uuid.UUID) -> bool:
    """
    Удаляет продукт из базы данных.

    Args:
        session (AsyncSession): Сессия базы данных.
        product_id (uuid.UUID): Идентификатор продукта, который нужно удалить.

    Returns:
        bool: True, если продукт успешно удален, False в случае ошибки.

    Raises:
        Exception: Если произошла ошибка при удалении продукта.
    """
    try:
        product = (await session.scalars(select(Product).where(Product.id == product_id))).one_or_none()

        if product:
            await session.execute(delete(Product).where(Product.id == product_id))
            await session.commit()
            return True
        else:
            logger.error(f"Продукт с id {product_id} не найден.")
            return False
    except Exception as e:
        logger.error(f"Произошла ошибка при удалении продукта: {e}")
        await session.rollback()
        return False


async def get_all_products(session: AsyncSession) -> List[Product]:
    """
    Получает список всех продуктов.

    Args:
        session (AsyncSession): Сессия базы данных.

    Returns:
        list[Product]: Список всех продуктов или пустой список в случае ошибки.

    Raises:
        Exception: Если произошла ошибка при получении списка продуктов.
    """
    try:
        products = (await session.execute(select(Product))).scalars().all()

        return products
    except Exception as e:
        logger.error(f"Произошла ошибка при получении списка продуктов: {e}")
        return []


async def update_cart_product(
        session: AsyncSession,
        product_id: uuid.UUID,
        quantity: int,
        user_id: uuid.UUID
) -> Optional[OrderInfo]:
    """
    Обновляет количество продукта в корзине.

    Args:
        session (AsyncSession): Сессия базы данных.
        product_id (uuid.UUID): Идентификатор продукта в корзине.
        quantity (int): Новое количество продукта.
        user_id (uuid.UUID): Идентификатор юзера.

    Returns:
        Optional[OrderInfo]: Обновленная информация о корзине пользователя или None в случае ошибки.

    Raises:
        Exception: Если произошла ошибка при обновлении продукта в корзине.
    """
    try:
        order_product = (
            await session.scalars(
                select(OrderProduct).join(Order).where(
                    Order.status == 'cart',
                    OrderProduct.product_id == product_id,
                    Order.user_id == user_id
                )
            )
        ).one_or_none()

        if order_product:
            order_product.quantity = quantity
            await session.commit()

            updated_order = await get_cart(session, order_product.order_id, user_id)
            return updated_order
        else:
            logger.error(f"Продукт с id {product_id} не найден в корзине.")
            return None
    except Exception as e:
        logger.error(f"Произошла ошибка при обновлении продукта в корзине: {e}")
        await session.rollback()
        return None


async def remove_from_cart(session: AsyncSession, product_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """
    Удаляет продукт из корзины.

    Args:
        session (AsyncSession): Сессия базы данных.
        product_id (uuid.UUID): Идентификатор продукта в корзине.
        user_id (uuid.UUID): Идентификатор пользователя.

    Returns:
        bool: True, если продукт успешно удален из корзины, False в случае ошибки.

    Raises:
        Exception: Если произошла ошибка при удалении продукта из корзины.
    """
    try:
        order_product = (
            await session.scalars(
                select(OrderProduct).join(Order).where(
                    Order.status == 'cart',
                    OrderProduct.product_id == product_id,
                    Order.user_id == user_id
                )
            )
        ).one_or_none()

        if order_product:
            await session.execute(delete(OrderProduct).where(
                OrderProduct.product_id == order_product.product_id
            ))
            await session.commit()

            return True
        else:
            logger.error(f"Продукт с id {product_id} не найден в корзине.")
            return False
    except Exception as e:
        logger.error(f"Произошла ошибка при удалении продукта из корзины: {e}")
        await session.rollback()
        return False


async def get_cart(session: AsyncSession, order_id: uuid.UUID, user_id: uuid.UUID) -> Optional[OrderInfo]:
    """
    Получает информацию о корзине пользователя.

    Args:
        session (AsyncSession): Сессия базы данных.
        order_id (uuid.UUID): Идентификатор заказа (корзины).
        user_id (uuid.UUID): Идентификатор пользователя.

    Returns:
        Optional[OrderInfo]: Информация о корзине пользователя или None в случае ошибки.

    Raises:
        Exception: Если произошла ошибка при получении информации о корзине.
    """
    try:
        order = (await session.scalars(select(Order).where(Order.id == order_id, Order.user_id == user_id))).one_or_none()

        if order:
            order_info = OrderInfo(status=order.status, user_id=order.user_id)
            return order_info
        else:
            logger.error(f"Корзина с id {order_id} не найдена.")
            return None
    except Exception as e:
        logger.error(f"Произошла ошибка при получении информации о корзине: {e}")
        return None
