from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from webapp.api.crud.recipe.router import recipe_router
from webapp.crud.crud import update
from webapp.db.postgres import get_session
from webapp.schema.recipe import RecipeData, RecipeResponse, RecipeTitle
from webapp.models.sirius.recipe import Recipe


@recipe_router.post(
    '/update/{recipe_id}',
    response_model=RecipeResponse,
)
async def update_recipe(
    recipe_id: int,
    body: RecipeTitle,
    session: AsyncSession = Depends(get_session)
    ) -> ORJSONResponse:
    updated_id = await update(session, recipe_id, body, Recipe)

    if updated_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


    return ORJSONResponse(
        {
            'id': updated_id,
            'title': body.title
        }
    )


