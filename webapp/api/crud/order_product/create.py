from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.order_product.router import op_router
from webapp.crud.order_product import op_crud
from webapp.db.postgres import get_session
from webapp.schema.info.order_product import OPInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@op_router.post('/create')
async def create_op(
    body: OPInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        await op_crud.create(session, body)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={'message': 'OP created successfully'}, status_code=status.HTTP_201_CREATED)
