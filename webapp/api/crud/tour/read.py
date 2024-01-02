from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.tour.router import tour_router
from webapp.api.crud.tour.utils.get_tour import get_tour_model
from webapp.crud.tour import tour_crud
from webapp.integrations.cache.cache import redis_get, redis_set
from webapp.integrations.postgres import get_session
from webapp.models.sirius.tour import Tour
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth
from webapp.utils.crud.serializers import serialize_model


@tour_router.get('/tour')
async def get_tour(
    tour_id: int | None = None,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if tour_id is None:
        serialized_tours = serialize_model(list(await tour_crud.get_all(session)))
        return ORJSONResponse({'tours': serialized_tours})

    if cached := (await redis_get(Tour.__name__, tour_id)):
        return ORJSONResponse({'cached_tour': cached})

    tour = await get_tour_model(session, tour_id)
    if tour is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_tour = serialize_model(tour)
    await redis_set(Tour.__name__, tour_id, serialized_tour)

    return ORJSONResponse({'tour': serialized_tour})
