from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.router import crud_router
from webapp.crud.reservation import reservation_crud
from webapp.integrations.postgres import get_session
from webapp.schema.info.reservation import ReservationInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@crud_router.get('/reservation/update')
async def get_users(
    body: ReservationInfo,
    reservation_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    reservation = await reservation_crud.get(session, reservation_id)  # type: ignore
    if reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await reservation_crud.update(session, reservation_id, body)

    return ORJSONResponse(
        content={'message': 'Reservation removed successfully'}, status_code=status.HTTP_204_NO_CONTENT
    )
