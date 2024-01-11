from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.order_product.router import op_router
from webapp.crud.order_product import op_crud
from webapp.db.postgres import get_session
from webapp.integrations.cache.cache import redis_get, redis_set
from webapp.models.sirius.order_product import OrderProduct
from webapp.schema.info.order_product import OPInfo, OPResponse, OPsListResponse
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@op_router.get('/page/{page}', response_model=OPsListResponse)
async def ops_get(
    page: int,
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    serialized_ops = [OPInfo.model_validate(op).model_dump() for op in await op_crud.get_page(session, page)]
    return ORJSONResponse({'ops': serialized_ops}, status_code=status.HTTP_200_OK)


@op_router.get('/{op_id}', response_model=OPResponse)
async def get_cached_op(
    op_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if cached := (await redis_get(OrderProduct.__name__, op_id)):
        return ORJSONResponse({'cached_op': cached})

    op = await op_crud.get_model(session, op_id)

    if op is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    serialized_op = OPInfo(**op.__dict__).model_dump(mode='json')
    await redis_set(OrderProduct.__name__, op_id, serialized_op)

    return ORJSONResponse({'op': serialized_op}, status_code=status.HTTP_200_OK)
