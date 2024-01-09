from fastapi import HTTPException
from fastapi.responses import ORJSONResponse
from starlette import status

from webapp.api.crud.ingredient.router import ingredient_router
from webapp.crud.crud import update
from webapp.db.postgres import get_session
from webapp.schema.ingredient import IngredientData, IngredientResponse, INGREDIENT_TABLE


@ingredient_router.post(
    '/update/{ingredient_id}',
    response_model=IngredientResponse,
)
async def update_ingredient(ingredient_id: int, body: IngredientData) -> ORJSONResponse:
    session = get_session()
    update(session, ingredient_id, body, INGREDIENT_TABLE)

    return ORJSONResponse(
        {
            'id': ingredient_id,
            'title': body.title
        }
    )
