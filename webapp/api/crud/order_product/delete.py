from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.order_product.router import op_router
from webapp.crud.order_product import op_crud
from webapp.db.postgres import get_session
from webapp.integrations.cache.cache import redis_drop_key
from webapp.models.sirius.order_product import OrderProduct
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@op_router.post('/delete/{op_id}')
async def delete_op(
    op_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> Response:
    if not await op_crud.delete(session, op_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await redis_drop_key(OrderProduct.__name__, op_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
