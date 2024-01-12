from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from orjson import dumps
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.crud.recipe.router import recipe_router
from webapp.crud.crud import get
from webapp.crud.get_ingredient import get_ingredient
from webapp.crud.get_recipe import get_recipe
from webapp.crud.ingredient_to_recipe import create_relationship
from webapp.db.postgres import get_session
from webapp.schema.recipe import RecipeData, RecipeResponse, RecipeIngredient, RecipeTitle, RecipeId
from webapp.api.crud.ingredient.create import create_ingredient
from webapp.api.crud.ingredient.read import read_ingredient
from webapp.models.sirius.recipe import Recipe
from webapp.models.sirius.ingredient_to_recipe import ingredient_to_recipe
from webapp.models.sirius.ingredient import Ingredient
from webapp.schema.ingredient import IngredientData
from webapp.schema.ingredient_to_recipe import AssociationData


@recipe_router.post(
    '/add_ingredient/{recipe_id}',
    response_model=RecipeResponse,
)
async def add_ingredient(
    recipe_id: int,
    body: RecipeIngredient,
    session: AsyncSession = Depends(get_session)
    ) -> ORJSONResponse:

    data = IngredientData(title=body.ingredient)
    ingredient = await get_ingredient(session, data)

    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Ingredient {body.ingredient} does not exist'
        )

    data = RecipeId(id=recipe_id)
    recipe = await get(session, data, Recipe)

    data = AssociationData(
        ingredient_id=ingredient.id,
        recipe_id=recipe.id
    )
    await create_relationship(session, data, ingredient_to_recipe)

    return ORJSONResponse(
        {
            'id': recipe.id,
            'title': recipe.title
        }
    )

