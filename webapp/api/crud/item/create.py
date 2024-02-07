from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.crud.item.router import item_router
from webapp.crud.crud import create
from webapp.db.postgres import get_session
from webapp.models.sirius.item import Item
from webapp.schema.item import ItemData, ItemResponse


@item_router.post(
    '/create',
    response_model=ItemResponse,
)
async def create_item(body: ItemData, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    item = await create(session, body, Item)

    return ORJSONResponse({'id': item.id, 'name': item.name})