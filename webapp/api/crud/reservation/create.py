from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.reservation.router import reservation_router
from webapp.crud.reservation import reservation_crud
from webapp.integrations.postgres import get_session
from webapp.schema.info.reservation import ReservationInfo
from webapp.utils.auth.jwt import oauth2_scheme


@reservation_router.post('/')
async def create_reservation(
    body: ReservationInfo,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    try:
        await reservation_crud.create(session, body)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={'message': 'Reservation created successfully'}, status_code=status.HTTP_201_CREATED)
