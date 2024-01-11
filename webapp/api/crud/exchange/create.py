from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.crud.exchange.router import exchange_router
from webapp.crud.crud import create
from webapp.db.postgres import get_session
from webapp.schema.exchange import ExchangeData, ExchangeResponse
from webapp.models.sirius.exchange import Exchange

@exchange_router.post(
    '/create',
    response_model=ExchangeResponse,
)
async def create_exchange(
    body: ExchangeData,
    session: AsyncSession = Depends(get_session)
    ) -> ORJSONResponse:
    
    exchange = await create(session, body, Exchange)

    return ORJSONResponse(
        {
            "id": exchange.id,
            "title": exchange.title
        }
    )