from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.crud.recipe.router import recipe_router
from webapp.crud.crud import create
from webapp.db.postgres import get_session
from webapp.schema.recipe import RecipeData, RecipeResponse, RECIPE_TABLE
from webapp.api.crud.ingredient.create import create as create_ingredient
from webapp.models.sirius.recipe import Recipe


@recipe_router.post(
    '/create',
    response_model=RecipeResponse,
)
async def create_recipe(
    body: RecipeData,
    session: AsyncSession = Depends(get_session)
    ) -> ORJSONResponse:
    ingredients = []
    for ingredient_title in body.ingredients:
        req = {'title': ingredient_title}
        ingredient_id = create_ingredient(req).id
        ingredients.append(ingredient_id)
    try:
        recipe_id = await create(session, body.title, Recipe)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    ingredient_to_recipe = 'ingredient_to_recipe'
    for ingredient_id in ingredients:
        data = {'ingredient_id': ingredient_id, 'recipe_id': recipe_id}
        create(session, data, ingredient_to_recipe)

    return ORJSONResponse(
        {
            'id': recipe_id,
            'title': body.title,
            'ingredients': body.ingredients
        }
    )
