from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.ingredient.router import ingredient_router
from webapp.crud.get_ingredient import get_ingredient
from webapp.db.postgres import get_session
from webapp.schema.ingredient import IngredientData, IngredientResponse


@ingredient_router.get(
    '/read',
    response_model=IngredientResponse,
)
async def read_ingredient(
    body: IngredientData,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    ingredient = await get_ingredient(session, body)

    if ingredient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(
        {
            'id': ingredient.id,
            'title': body.title
        }
    )
