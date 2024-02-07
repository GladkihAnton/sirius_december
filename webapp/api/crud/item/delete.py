from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.item.router import item_router
from webapp.crud.crud import delete
from webapp.db.postgres import get_session
from webapp.models.sirius.item import Item
from webapp.schema.item import ItemData


@item_router.post(
    '/delete/{item_id}',
    response_model=ItemData,
)
async def delete_item(item_id: int, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    deleted_id = await delete(session, item_id, Item)

    if deleted_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse({'id': deleted_id})