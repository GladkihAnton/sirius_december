from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.metrics import async_integrations_timer
from webapp.models.sirius.ingredient import Ingredient
from webapp.schema.ingredient import IngredientData


@async_integrations_timer
async def get_ingredient(session: AsyncSession, ingredient_data: IngredientData) -> Ingredient | None:
    return (await session.scalars(select(Ingredient).where(Ingredient.title == ingredient_data.title))).one_or_none()
