from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.reservation.router import reservation_router
from webapp.crud.reservation import reservation_crud
from webapp.integrations.cache.cache import redis_drop_key
from webapp.integrations.postgres import get_session
from webapp.models.sirius.reservation import Reservation
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@reservation_router.delete('/{reservation_id}')
async def delete_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> Response:
    if not await reservation_crud.delete(session, reservation_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await redis_drop_key(Reservation.__name__, reservation_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
