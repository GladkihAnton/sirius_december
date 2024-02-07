from fastapi import Depends, HTTPException, Path
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.exchange.router import exchange_router
from webapp.crud.crud import get_all
from webapp.crud.get_exchange import get_exchange
from webapp.db.postgres import get_session
from webapp.models.sirius.exchange import Exchange
from webapp.schema.exchange import ExchangeData, ExchangeResponse, ExchangesResponse


@exchange_router.get(
    '/read/{exchange_id}',
    response_model=ExchangeResponse,
)
async def read_exchange(
    exchange_id: int = Path(..., title="ID обмена"),
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    exchange = await get_exchange(session, exchange_id)

    if exchange is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse({'id': exchange.id, 'item1_id': exchange.item1_id, 'item2_id': exchange.item2_id})

@exchange_router.get(
    '/read_all',
    response_model=ExchangesResponse,
)
async def read_exchanges(
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    exchanges = await get_all(session, Exchange)

    return ORJSONResponse([{'id': exchange.id, 'item1_id': exchange.item1_id, 'item2_id': exchange.item2_id} for exchange in exchanges])