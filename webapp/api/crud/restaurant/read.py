from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.restaurant.router import restaurant_router
from webapp.crud.restaurant import restaurant_crud
from webapp.db.postgres import get_session
from webapp.integrations.cache.cache import redis_get, redis_set
from webapp.models.sirius.restaurant import Restaurant
from webapp.schema.info.restaurant import RestaurantInfo, RestaurantResponse, RestaurantsListResponse
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@restaurant_router.get('/page/{page}', response_model=RestaurantsListResponse)
async def restaurants_get(
    page: int,
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    serialized_restaurants = [
        RestaurantInfo.model_validate(restaurant).model_dump()
        for restaurant in await restaurant_crud.get_page(session, page)
    ]
    return ORJSONResponse({'restaurants': serialized_restaurants}, status_code=status.HTTP_200_OK)


@restaurant_router.get('/{restaurant_id}', response_model=RestaurantResponse)
async def get_cached_restaurant(
    restaurant_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if cached := (await redis_get(Restaurant.__name__, restaurant_id)):
        return ORJSONResponse({'cached_restaurant': cached})

    restaurant = await restaurant_crud.get_model(session, restaurant_id)

    if restaurant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_restaurant = RestaurantInfo(**restaurant.__dict__).model_dump(mode='json')
    await redis_set(Restaurant.__name__, restaurant_id, serialized_restaurant)

    return ORJSONResponse({'restaurant': serialized_restaurant}, status_code=status.HTTP_200_OK)
