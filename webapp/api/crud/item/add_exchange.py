from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from orjson import dumps
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.crud.item.router import item_router
from webapp.crud.crud import get
from webapp.crud.get_item import get_item
from webapp.crud.exchange_to_item import create_relationship
from webapp.db.postgres import get_session
from webapp.schema.item import ItemData, ItemResponse, ItemExchange, ItemTitle, ItemId
from webapp.api.crud.exchange.create import create_exchange
from webapp.api.crud.exchange.read import read_exchange
from webapp.models.sirius.item import Item
from webapp.models.sirius.exchange_to_item import exchange_to_item
from webapp.models.sirius.exchange import Exchange
from webapp.schema.exchange import ExchangeData
from webapp.schema.exchange_to_item import AssociationData


@item_router.post(
    '/add_exchange/{item_id}',
    response_model=ItemResponse,
)
async def add_exchange(
    item_id: int,
    body: ItemExchange,
    session: AsyncSession = Depends(get_session)
    ) -> ORJSONResponse:

    data = ExchangeData(title=body.exchange)
    exchange = await get_exchange(session, data)

    if exchange is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Exchange {body.exchange} does not exist'
        )

    data = ItemId(id=item_id)
    item = await get_item(session, data, Item)

    data = AssociationData(
        exchange_id=exchange.id,
        item_id=item.id
    )
    await create_relationship(session, data, exchange_to_item)

    return ORJSONResponse(
        {
            'id': item.id,
            'title': item.title
        }
    )
