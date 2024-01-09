from fastapi import HTTPException
from fastapi.responses import ORJSONResponse
from starlette import status

from webapp.api.crud.recipe.router import recipe_router
from webapp.crud.crud import delete
from webapp.db.postgres import get_session
from webapp.schema.recipe import RecipeData, RECIPE_TABLE


@recipe_router.post(
    '/delete/{recipe_id}',
    response_model=ORJSONResponse,
)
async def delete_recipe(recipe_id: int) -> int:
    session = get_session()
    try:
        delete(session, recipe_id, RECIPE_TABLE)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return ORJSONResponse(
        {
            'id': recipe_id
        }
    )
