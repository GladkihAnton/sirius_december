from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.ingredient.router import ingredient_router
from webapp.crud.crud import update
from webapp.db.postgres import get_session
from webapp.models.sirius.ingredient import Ingredient
from webapp.schema.ingredient import IngredientData, IngredientResponse


@ingredient_router.post(
    '/update/{ingredient_id}',
    response_model=IngredientResponse,
)
async def update_ingredient(
    ingredient_id: int, body: IngredientData, session: AsyncSession = Depends(get_session)
) -> ORJSONResponse:
    updated_id = await update(session, ingredient_id, body, Ingredient)

    if updated_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse({'id': updated_id, 'title': body.title})
