from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.exchange.router import exchange_router
from webapp.crud.crud import delete
from webapp.db.postgres import get_session
from webapp.models.sirius.exchange import Exchange
from webapp.schema.exchange import ExchangeData


@exchange_router.post(
    '/delete/{exchange_id}',
    response_model=ExchangeData,
)
async def delete_exchange(exchange_id: int, session: AsyncSession = Depends(get_session)) -> ORJSONResponse:
    deleted_id = await delete(session, exchange_id, Exchange)

    if deleted_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse({'id': deleted_id})