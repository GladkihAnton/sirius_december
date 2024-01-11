from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.order.router import order_router
from webapp.crud.order import order_crud
from webapp.db.postgres import get_session
from webapp.schema.info.order import OrderInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@order_router.post('/create')
async def create_order(
    body: OrderInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        await order_crud.create(session, body)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={'message': 'Order created successfully'}, status_code=status.HTTP_201_CREATED)
