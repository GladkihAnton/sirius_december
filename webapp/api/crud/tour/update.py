from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.tour.router import tour_router
from webapp.crud.tour import tour_crud
from webapp.integrations.postgres import get_session
from webapp.schema.auth.tour import TourInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@tour_router.post('/update/{tour_id}')
async def update_tour(
    body: TourInfo,
    tour_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if await tour_crud.update(session, tour_id, body) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(content={'message': 'Tour updated successfully'}, status_code=status.HTTP_204_NO_CONTENT)
