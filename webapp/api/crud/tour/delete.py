from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.tour.router import tour_router
from webapp.crud.tour import tour_crud
from webapp.integrations.cache.cache import redis_drop_key
from webapp.integrations.postgres import get_session
from webapp.models.sirius.tour import Tour
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@tour_router.post('/delete/{tour_id}')
async def delete_tour(
    tour_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> Response:
    if not await tour_crud.delete(session, tour_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await redis_drop_key(Tour.__name__, tour_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
