from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.item.router import item_router
from webapp.crud.crud import update
from webapp.db.postgres import get_session
from webapp.models.sirius.item import Item
from webapp.schema.item import ItemData, ItemResponse


@item_router.post(
    '/update/{item_id}',
    response_model=ItemResponse,
)
async def update_item(
    item_id: int, body: ItemData, session: AsyncSession = Depends(get_session)
) -> ORJSONResponse:
    updated_id = await update(session, item_id, body, Item)

    if updated_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse({'id': updated_id, 'name': body.name})