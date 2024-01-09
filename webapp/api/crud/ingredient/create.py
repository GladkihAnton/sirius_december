from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.crud.ingredient.router import ingredient_router
from webapp.crud.crud import create
from webapp.db.postgres import get_session
from webapp.schema.ingredient import IngredientData, IngredientResponse
from webapp.schema.ingredient import INGREDIENT_TABLE
from webapp.models.sirius.ingredient import Ingredient



@ingredient_router.post(
    '/create',
    response_model=IngredientResponse,
)
async def create_ingredient(
    body: IngredientData,
    session: AsyncSession = Depends(get_session)
    ) -> ORJSONResponse:
    ingredient_id = await create(session, body, Ingredient)

    return ingredient_id
