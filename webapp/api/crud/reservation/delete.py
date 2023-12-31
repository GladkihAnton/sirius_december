from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.router import crud_router
from webapp.crud.reservation import reservation_crud
from webapp.integrations.postgres import get_session
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@crud_router.get('/reservation/delete')
async def delete_review(
    reservation_id: int | None = None,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    reservation = await reservation_crud.get(session, reservation_id)  # type: ignore
    if reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await reservation_crud.delete(session, reservation_id)

    return ORJSONResponse(
        content={'message': 'Reservation removed successfully'}, status_code=status.HTTP_204_NO_CONTENT
    )
