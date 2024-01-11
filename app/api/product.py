import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from loguru import logger
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import orjson

from app.api.log_route import LogRoute
from app.db import crud, session
from app.schemas.schema import ProductInfo
from app.cache.cache import redis_set, redis_get, redis_drop_key

router = APIRouter(route_class=LogRoute)


@router.post("/create_product", response_model=ProductInfo, status_code=status.HTTP_201_CREATED)
async def create_product(product_info: ProductInfo, db: AsyncSession = Depends(session.get_db)) -> ProductInfo: 
    """
    Создание нового продукта.

    Args:
        product_info (ProductInfo): Информация о новом продукте.
        db (AsyncSession): Сессия базы данных.

    Returns:
        ProductInfo: Созданный продукт.

    Raises:
        HTTPException: Если произошла ошибка при создании продукта.
    """
    try:
        created_product = await crud.create_product(db, product_info)

        if created_product is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create product")
        await redis_drop_key("products", "all_products")
        return ORJSONResponse(ProductInfo.model_validate(created_product).model_dump())
    except Exception as e:
        logger.error(f"Произошла ошибка во время создания продукта: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.put("/update_product/{product_id}", response_model=ProductInfo, status_code=status.HTTP_200_OK)
async def update_product(product_id: uuid.UUID, updated_info: ProductInfo, db: AsyncSession = Depends(session.get_db)) -> ProductInfo:
    """
    Обновление информации о продукте.

    Args:
        product_id (uuid.UUID): Идентификатор продукта, который нужно обновить.
        updated_info (ProductInfo): Новая информация о продукте.
        db (AsyncSession): Сессия базы данных.

    Returns:
        ProductInfo: Обновленный продукт.

    Raises:
        HTTPException: Если произошла ошибка при обновлении продукта.
    """
    try:
        updated_product = await crud.update_product(db, product_id, updated_info)

        if updated_product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found")
        await redis_drop_key("products", "all_products")
        return ProductInfo(name=updated_product.name, description=updated_product.description, price=updated_product.price)
    except Exception as e:
        logger.error(f"Произошла ошибка во время обновления продукта: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.delete("/delete_product/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: uuid.UUID, db: AsyncSession = Depends(session.get_db)) -> None:
    """
    Удаление продукта.

    Args:
        product_id (uuid.UUID): Идентификатор продукта, который нужно удалить.
        db (AsyncSession): Сессия базы данных.

    Raises:
        HTTPException: Если произошла ошибка при удалении продукта.
    """
    try:
        result = await crud.delete_product(db, product_id)

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found")
        await redis_drop_key("products", "all_products")
    except Exception as e:
        logger.error(f"Произошла ошибка во время удаления продукта: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/get_all_products", response_model=list[ProductInfo], status_code=status.HTTP_200_OK)
async def get_all_products(db: AsyncSession = Depends(session.get_db)) -> List[ProductInfo]:
    """
    Получение списка всех продуктов.

    Args:
        db (AsyncSession): Сессия базы данных.

    Returns:
        list[ProductInfo]: Список всех продуктов.

    Raises:
        HTTPException: Если произошла ошибка при получении списка продуктов.
    """
    try:
        products = await redis_get('products', "all_products")
        if products:
            return [ProductInfo(**product) for product in products["products"]]

        products = await crud.get_all_products(db)

        if not products:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found")
        products_data = [{"name": product.name, "description": product.description, "price": product.price} for product in products]
        await redis_set("products", "all_products", {"products": products_data})
        return products_data
    except Exception as e:
        logger.error(f"Произошла ошибка во время получения списка продуктов: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
