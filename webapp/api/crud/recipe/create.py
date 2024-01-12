from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.crud.recipe.router import recipe_router
from webapp.crud.crud import create
from webapp.db.postgres import get_session
from webapp.schema.recipe import RecipeData, RecipeResponse, RecipeTitle, RecipeIngredient
from webapp.api.crud.recipe.add_ingredient import add_ingredient
from webapp.models.sirius.recipe import Recipe

@recipe_router.post(
    '/create',
    response_model=RecipeResponse,
)
async def create_recipe(
    body: RecipeData,
    session: AsyncSession = Depends(get_session)
    ) -> ORJSONResponse:

    data = RecipeTitle(title=body.title)
    recipe = await create(session, data, Recipe)

    for ingredient_title in body.ingredients:
        ingredient = RecipeIngredient(ingredient=ingredient_title)
        await add_ingredient(recipe.id, ingredient, session)

    return ORJSONResponse(
        {
            'id': recipe.id,
            'title': recipe.title
        }
    )

