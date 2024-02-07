from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.crud.exchange.router import exchange_router
from webapp.crud.crud import create
from webapp.db.postgres import get_session
from webapp.models.sirius.exchange import Exchange
from webapp.schema.exchange import ExchangeData, ExchangeResponse


@exchange_router.post(
    '/create',
    response_model=ExchangeResponse,
)
async def create_exchange(body: ExchangeData, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:

    exchange = await create(session, body, Exchange)

    return ORJSONResponse({"id": exchange.id, 
                           "item1_id": exchange.item1_id, 
                           "item2_id": exchange.item2_id
                           })
