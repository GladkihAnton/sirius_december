from fastapi import Depends, Body, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.chouse_restaurant.router import restaurants_router
from webapp.crud.restaurant import get_restaurants
from webapp.db.postgres import get_session
from webapp.schema.restaurant.restaurant import RestaurantsList, RestaurantsListResponse
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


# TODO Проверить falke8 и включить авторизацию
@restaurants_router.get(
    '/list',
    response_model=RestaurantsListResponse,
)
async def rlist(
        body: RestaurantsList = Body(default=None),
        # access_token: JwtTokenT = Depends(jwt_auth.validate_token),
        session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    res = await get_restaurants(session, body)
    if len(res) != 0:
        res_as_lists = [[r.id, r.name, r.location] for r in res]
        return ORJSONResponse(
            {
                'r_list': res_as_lists,
            }
        )
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT)

