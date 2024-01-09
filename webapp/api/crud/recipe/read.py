from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.recipe.router import recipe_router
from webapp.crud.get_recipe import get_recipe
from webapp.db.postgres import get_session
from webapp.schema.recipe import RecipeData, RecipeResponse


@recipe_router.get(
    '/read',
    response_model=RecipeResponse,
)
async def read_recipe(
    body: RecipeData,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    recipe = await get_recipe(session, body)

    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(
        {
            'id': recipe.id,
            'title': body.title,
            'ingredients': body.ingredients
        }
    )
