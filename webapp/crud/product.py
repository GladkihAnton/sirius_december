from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from webapp.crud.utils.operations import AsyncCRUDFactory, get_entities_by_name
from webapp.models.sirius.product import Product
from webapp.schema.info.product import ProductSearch

product_crud = AsyncCRUDFactory(Product)


async def get_products(session: AsyncSession, product_info: ProductSearch) -> Sequence[Product]:
    return await get_entities_by_name(session, Product, product_info)
