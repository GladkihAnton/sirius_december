from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.v1.router import v1_router
from webapp.crud.restaurant import get_restaurants
from webapp.db.postgres import get_session
from webapp.schema.info.restaurant import RestaurantInfo, RestaurantSearch, RestaurantsListResponse
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@v1_router.get('/restaurants_search', response_model=RestaurantsListResponse)
async def restaurants_search(
    body: RestaurantSearch,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    serialized_restaurants = [
        RestaurantInfo.model_validate(restaurant).model_dump() for restaurant in await get_restaurants(session, body)
    ]

    if not serialized_restaurants:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse({'restaurants': serialized_restaurants}, status_code=status.HTTP_200_OK)
