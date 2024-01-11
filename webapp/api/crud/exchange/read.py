from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import List

from webapp.api.crud.exchange.router import exchange_router
from webapp.crud.crud import get_all
from webapp.crud.get_exchange import get_exchange
from webapp.db.postgres import get_session
from webapp.schema.exchange import ExchangeData, ExchangeResponse, ExchangesResponse
from webapp.models.sirius.exchange import Exchange

@exchange_router.get(
    '/read',
    response_model=ExchangeResponse,
)
async def read_exchange(
    body: ExchangeData,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    exchange = await get_exchange(session, body)

    if exchange is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(
        {
            'id': exchange.id,
            'title': exchange.title
        }
    )

@exchange_router.get(
    '/read_all',
    response_model=ExchangesResponse,
)
async def read_exchanges(session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    exchanges = await get_all(session, Exchange)

    return ORJSONResponse(
        [{
            'id': exchange.id,
            'title': exchange.title
        } for exchange in exchanges] 
    )