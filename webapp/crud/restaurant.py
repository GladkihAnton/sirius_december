from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.sirius.restaurant import Restaurant
from webapp.schema.restaurant.restaurant import RestaurantsList


async def get_restaurants(session: AsyncSession, restaurant_info: RestaurantsList) -> Sequence[Restaurant]:
    query = select(Restaurant)
    if restaurant_info:
        query = query.where(Restaurant.name == restaurant_info.name)
    return (await session.execute(query)).scalars().all()
