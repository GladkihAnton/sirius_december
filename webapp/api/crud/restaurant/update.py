from fastapi import Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.restaurant.router import restaurant_router
from webapp.crud.restaurant import restaurant_crud
from webapp.db.postgres import get_session
from webapp.integrations.cache.cache import redis_drop_key
from webapp.models.sirius.restaurant import Restaurant
from webapp.schema.info.restaurant import RestaurantInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@restaurant_router.post('/update/{restaurant_id}')
async def update_restaurant(
    body: RestaurantInfo,
    restaurant_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> Response:
    existing_restaurant = await restaurant_crud.get_model(session, restaurant_id)

    if existing_restaurant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    updated_restaurant = await restaurant_crud.update(session, restaurant_id, body)

    await redis_drop_key(Restaurant.__name__, restaurant_id)

    if updated_restaurant:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(content={'message': 'Restaurant created successfully'}, status_code=status.HTTP_201_CREATED)
