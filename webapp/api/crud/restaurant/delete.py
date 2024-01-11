from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.restaurant.router import restaurant_router
from webapp.crud.restaurant import restaurant_crud
from webapp.db.postgres import get_session
from webapp.integrations.cache.cache import redis_drop_key
from webapp.models.sirius.restaurant import Restaurant
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@restaurant_router.post('/delete/{restaurant_id}')
async def delete_restaurant(
    restaurant_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> Response:
    if not await restaurant_crud.delete(session, restaurant_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await redis_drop_key(Restaurant.__name__, restaurant_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
