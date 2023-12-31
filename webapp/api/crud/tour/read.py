from typing import List

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.router import crud_router
from webapp.crud.tour import tour_crud
from webapp.integrations.postgres import get_session
from webapp.models.sirius.user import User
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth
from webapp.utils.crud.serializers import serialize_model


@crud_router.get('/tour')
async def get_tour(
    tour_id: int | None = None,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if tour_id is None:
        tours: List[User] = list(await tour_crud.get_all(session))
        serialized_tours = serialize_model(tours)
        return ORJSONResponse({'tours': serialized_tours})

    tour = await tour_crud.get(session, tour_id)  # type: ignore
    if tour is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_tour = serialize_model(tour)
    return ORJSONResponse({'tour': serialized_tour})
