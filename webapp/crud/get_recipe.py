from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.sirius.recipe import Recipe
from webapp.schema.recipe import RecipeData


async def get_recipe(session: AsyncSession, recipe_data: RecipeData) -> Recipe | None:
    return (
        await session.scalars(
            select(Recipe).where(
                Recipe.title == recipe_data.title
            )
        )
    ).one_or_none()

