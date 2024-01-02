from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.login.router import auth_router
from webapp.crud.reservation import reservation_crud
from webapp.integrations.postgres import get_session
from webapp.schema.info.reservation import ReservationInfo


@auth_router.post('/reservation/create')
async def create_review(
    body: ReservationInfo,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    try:
        await reservation_crud.create(session, body)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={'message': 'Reservation created successfully'}, status_code=status.HTTP_201_CREATED)
