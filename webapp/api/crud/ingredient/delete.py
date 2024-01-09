from fastapi import HTTPException
from starlette import status
from fastapi.responses import ORJSONResponse

from webapp.api.crud.ingredient.router import ingredient_router
from webapp.crud.crud import delete
from webapp.db.postgres import get_session
from webapp.schema.ingredient import IngredientData, INGREDIENT_TABLE


@ingredient_router.post(
    '/delete/{ingredient_id}',
    response_model=ORJSONResponse,
)
async def delete_ingredient(ingredient_id: int) -> ORJSONResponse:
    session = get_session()
    delete(session, ingredient_id, INGREDIENT_TABLE)
    
    return ORJSONResponse(
        {
            'id': ingredient_id
        }
    )

