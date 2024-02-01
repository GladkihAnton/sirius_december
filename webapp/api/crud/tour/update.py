from typing import Annotated

from fastapi import Depends
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.tour.router import tour_router
from webapp.crud.tour import tour_crud
from webapp.integrations.cache.cache import redis_drop_key
from webapp.integrations.postgres import get_session
from webapp.models.sirius.tour import Tour
from webapp.schema.info.tour import TourInfo
from webapp.utils.auth.jwt import oauth2_scheme


@tour_router.put('/{tour_id}')
async def update_tour(
    body: TourInfo,
    tour_id: int,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> Response:
    exists = tour_crud.get_model(session, tour_id) is not None

    await tour_crud.update(session, tour_id, body)

    await redis_drop_key(Tour.__name__, tour_id)

    if exists:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return Response(content={'message': 'Tour created successfully'}, status_code=status.HTTP_201_CREATED)
