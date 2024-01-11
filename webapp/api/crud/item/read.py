from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import List

from webapp.api.crud.item.router import item_router
from webapp.crud.crud import get_all
from webapp.crud.get_item import get_item
from webapp.db.postgres import get_session
from webapp.schema.item import ItemData, ItemResponse, ItemsResponse
from webapp.models.sirius.item import Item

@item_router.get(
    '/read',
    response_model=ItemResponse,
)
async def read_item(
    body: ItemData,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    item = await get_item(session, body)

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(
        {
            'id': item.id,
            'title': item.title,
            'exchanges': item.exchanges
        }
    )

@item_router.get(
    '/read_all',
    response_model=ItemsResponse,
)
async def read_items(session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    items = await get_all(session, Item)

    return ORJSONResponse(
        [{
            'id': item.id,
            'title': item.title
        } for item in items] 
    )