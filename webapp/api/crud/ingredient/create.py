from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.crud.ingredient.router import ingredient_router
from webapp.crud.crud import create
from webapp.db.postgres import get_session
from webapp.models.sirius.ingredient import Ingredient
from webapp.schema.ingredient import IngredientData, IngredientResponse


@ingredient_router.post(
    '/create',
    response_model=IngredientResponse,
)
async def create_ingredient(body: IngredientData, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:

    ingredient = await create(session, body, Ingredient)

    return ORJSONResponse({"id": ingredient.id, "title": ingredient.title})
