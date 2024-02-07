from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.exchange.router import exchange_router
from webapp.crud.crud import update
from webapp.db.postgres import get_session
from webapp.models.sirius.exchange import Exchange
from webapp.schema.exchange import ExchangeData, ExchangeResponse


@exchange_router.post(
    '/update/{exchange_id}',
    response_model=ExchangeResponse,
)
async def update_exchange(
    exchange_id: int, body: ExchangeData, session: AsyncSession = Depends(get_session)
) -> ORJSONResponse:
    updated_id = await update(session, exchange_id, body, Exchange)

    if updated_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse({'id': updated_id, 'item1_id': body.item1_id, 'item2_id': body.item2_id})
