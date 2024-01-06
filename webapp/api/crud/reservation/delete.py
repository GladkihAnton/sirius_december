from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.reservation.router import reservation_router
from webapp.crud.reservation import reservation_crud
from webapp.integrations.postgres import get_session
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@reservation_router.post('/delete/{reservation_id}')
async def delete_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if not await reservation_crud.delete(session, reservation_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(
        content={'message': 'Reservation removed successfully'}, status_code=status.HTTP_204_NO_CONTENT
    )