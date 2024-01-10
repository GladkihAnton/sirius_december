from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.deal.router import deal_router
from webapp.crud.deal import deal_crud
from webapp.integrations.cache.cache import redis_get, redis_set
from webapp.integrations.postgres import get_session
from webapp.models.sirius.deal import Deal
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth
from webapp.utils.crud.serializers import serialize_model


@deal_router.get('/')
async def get_deals(
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    serialized_deals = serialize_model(list(await deal_crud.get_all(session)))
    return ORJSONResponse({'deals': serialized_deals})


@deal_router.get('/{deal_id}')
async def get_cached_deal(
    deal_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if cached := (await redis_get(Deal.__name__, deal_id)):
        return ORJSONResponse({'cached_deal': cached})

    deal = await deal_crud.get_model(session, deal_id)
    if deal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_deal = serialize_model(deal)
    await redis_set(Deal.__name__, deal_id, serialized_deal)

    return ORJSONResponse({'deal': serialized_deal})
