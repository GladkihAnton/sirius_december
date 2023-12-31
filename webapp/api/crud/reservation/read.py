from typing import List

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.router import crud_router
from webapp.crud.reservation import reservation_crud
from webapp.crud.tour import tour_crud
from webapp.integrations.postgres import get_session
from webapp.models.sirius.reservation import Reservation
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth
from webapp.utils.crud.serializers import serialize_model


@crud_router.get('/reservation')
async def get_review(
    reservation_id: int | None = None,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if reservation_id is None:
        reservations: List[Reservation] = list(await reservation_crud.get_all(session))
        serialized_reservations = serialize_model(reservations)
        return ORJSONResponse({'reservations': serialized_reservations})

    reservation = await tour_crud.get(session, reservation_id)  # type: ignore
    if reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_reservation = serialize_model(reservation)
    return ORJSONResponse({'reservation': serialized_reservation})
