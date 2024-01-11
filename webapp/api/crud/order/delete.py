from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.order.router import order_router
from webapp.crud.order import order_crud
from webapp.db.postgres import get_session
from webapp.integrations.cache.cache import redis_drop_key
from webapp.models.sirius.order import Order
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@order_router.post('/delete/{order_id}')
async def delete_order(
    order_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> Response:
    if not await order_crud.delete(session, order_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await redis_drop_key(Order.__name__, order_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
