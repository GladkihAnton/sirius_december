from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.tour.router import tour_router
from webapp.crud.tour import tour_crud
from webapp.integrations.cache.cache import redis_drop_key
from webapp.integrations.postgres import get_session
from webapp.models.sirius.tour import Tour
from webapp.schema.info.tour import TourInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@tour_router.post('/update/{tour_id}')
async def update_tour(
    body: TourInfo,
    tour_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    exists = tour_crud.get_model(session, tour_id) is not None

    await tour_crud.update(session, tour_id, body)

    await redis_drop_key(Tour.__name__, tour_id)

    if exists:
        return ORJSONResponse(content={'message': 'Tour updated successfully'}, status_code=status.HTTP_204_NO_CONTENT)

    return ORJSONResponse(content={'message': 'Tour created successfully'}, status_code=status.HTTP_201_CREATED)
