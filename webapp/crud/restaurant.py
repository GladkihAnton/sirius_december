from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from webapp.crud.utils.operations import AsyncCRUDFactory, get_entities_by_name
from webapp.models.sirius.restaurant import Restaurant
from webapp.schema.info.restaurant import RestaurantSearch

restaurant_crud = AsyncCRUDFactory(Restaurant)


async def get_restaurants(session: AsyncSession, restaurant_info: RestaurantSearch) -> Sequence[Restaurant]:
    return await get_entities_by_name(session, Restaurant, restaurant_info)
