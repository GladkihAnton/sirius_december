from fastapi import HTTPException
from fastapi.responses import ORJSONResponse
from starlette import status

from webapp.api.crud.recipe.router import recipe_router
from webapp.crud.crud import update
from webapp.db.postgres import get_session
from webapp.schema.recipe import RecipeData, RecipeResponse, RECIPE_TABLE


@recipe_router.post(
    '/update/{recipe_id}',
    response_model=RecipeResponse,
)
async def update_recipe(recipe_id: int, body: RecipeData) -> ORJSONResponse:
    session = get_session()
    update(session, recipe_id, body, RECIPE_TABLE)

    return ORJSONResponse(
        {
            'id': recipe_id,
            'title': body.title
        }
    )
