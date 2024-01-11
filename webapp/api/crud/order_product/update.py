from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.order_product.router import op_router
from webapp.crud.order_product import op_crud
from webapp.db.postgres import get_session
from webapp.integrations.cache.cache import redis_drop_key
from webapp.models.sirius.order_product import OrderProduct
from webapp.schema.info.order_product import OPInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@op_router.post('/update/{op_id}')
async def update_order(
    body: OPInfo,
    op_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> Response:
    existing_op = await op_crud.get_model(session, op_id)

    if existing_op is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    updated_op = await op_crud.update(session, op_id, body)

    await redis_drop_key(OrderProduct.__name__, op_id)

    if updated_op:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(content={'message': 'OP created successfully'}, status_code=status.HTTP_201_CREATED)
