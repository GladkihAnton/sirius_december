from typing import Annotated

from fastapi import Depends
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.reservation.router import reservation_router
from webapp.crud.reservation import reservation_crud
from webapp.integrations.cache.cache import redis_drop_key
from webapp.integrations.postgres import get_session
from webapp.models.sirius.reservation import Reservation
from webapp.schema.info.reservation import ReservationInfo
from webapp.utils.auth.jwt import oauth2_scheme


@reservation_router.put('/{reservation_id}')
async def update_reservation(
    body: ReservationInfo,
    reservation_id: int,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> Response:
    exists = reservation_crud.get_model(session, reservation_id) is not None

    await reservation_crud.update(session, reservation_id, body)

    await redis_drop_key(Reservation.__name__, reservation_id)

    if exists:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return Response(content={'message': 'Reservation created successfully'}, status_code=status.HTTP_201_CREATED)
