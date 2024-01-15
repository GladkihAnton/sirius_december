from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.recipe.router import recipe_router
from webapp.crud.crud import create, get
from webapp.crud.get_ingredient import get_ingredient
from webapp.db.postgres import get_session
from webapp.models.sirius.ingredient_to_recipe import IngredientToRecipe
from webapp.models.sirius.recipe import Recipe
from webapp.schema.ingredient import IngredientData
from webapp.schema.ingredient_to_recipe import AssociationData
from webapp.schema.recipe import RecipeIngredient, RecipeResponse


@recipe_router.post(
    '/add_ingredient/{recipe_id}',
    response_model=RecipeResponse,
)
async def add_ingredient(
    recipe_id: int, body: RecipeIngredient, session: AsyncSession = Depends(get_session)
) -> ORJSONResponse:

    data = IngredientData(title=body.ingredient)
    ingredient = await get_ingredient(session, data)

    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Ingredient {body.ingredient} does not exist'
        )

    recipe = await get(session, recipe_id, Recipe)

    data = AssociationData(ingredient_id=ingredient.id, recipe_id=recipe.id)
    await create(session, data, IngredientToRecipe)

    return ORJSONResponse({'id': recipe.id, 'title': recipe.title})
