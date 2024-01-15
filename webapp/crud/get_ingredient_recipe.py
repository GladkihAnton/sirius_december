from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.metrics import async_integrations_timer
from webapp.models.sirius.ingredient_to_recipe import IngredientToRecipe


@async_integrations_timer
async def get_ingredient_recipe(
    session: AsyncSession, ingredient_id: int = None, recipe_id: int = None
) -> IngredientToRecipe | None:
    if ingredient_id:
        query = IngredientToRecipe.ingredient_id == ingredient_id
    elif recipe_id:
        query = IngredientToRecipe.recipe_id == recipe_id
    return (await session.scalars(select(IngredientToRecipe).where(query))).one_or_none()
