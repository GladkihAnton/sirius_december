from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.reservation.router import reservation_router
from webapp.api.crud.reservation.utils.get_activity import get_reservation_model
from webapp.crud.reservation import reservation_crud
from webapp.integrations.cache.cache import redis_get, redis_set
from webapp.integrations.postgres import get_session
from webapp.models.sirius.reservation import Reservation
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth
from webapp.utils.crud.serializers import serialize_model


@reservation_router.get('/')
async def get_reservations(
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    serialized_reservations = serialize_model(list(await reservation_crud.get_all(session)))
    return ORJSONResponse({'reservations': serialized_reservations})


@reservation_router.get('/{reservation_id}')
async def get_review(
    reservation_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if cached := (await redis_get(Reservation.__name__, reservation_id)):
        return ORJSONResponse({'cached_reservation': cached})

    reservation = await get_reservation_model(session, reservation_id)
    if reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_reservation = serialize_model(reservation)
    await redis_set(Reservation.__name__, reservation_id, serialized_reservation)

    return ORJSONResponse({'reservation': serialized_reservation})
