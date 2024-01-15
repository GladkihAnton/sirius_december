from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.tour.router import tour_router
from webapp.crud.tour import tour_crud
from webapp.integrations.cache.cache import redis_get, redis_set
from webapp.integrations.postgres import get_session
from webapp.models.sirius.tour import Tour
from webapp.schema.info.tour import TourInfo
from webapp.utils.auth.jwt import oauth2_scheme


@tour_router.get('/page/{page}')
async def get_tours(
    page: int,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    serialized_tours = [TourInfo.model_validate(tour).model_dump() for tour in await tour_crud.get_page(session, page)]
    return ORJSONResponse({'tours': serialized_tours})


@tour_router.get('/{tour_id}')
async def get_cached_tour(
    tour_id: int,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    if cached := (await redis_get(Tour.__name__, tour_id)):
        return ORJSONResponse({'tour': cached})

    tour = await tour_crud.get_model(session, tour_id)
    if tour is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_tour = TourInfo.model_validate(tour).model_dump(mode='json')

    await redis_set(Tour.__name__, tour_id, serialized_tour)

    return ORJSONResponse({'tour': serialized_tour})
