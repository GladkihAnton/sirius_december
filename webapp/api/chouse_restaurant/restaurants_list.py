from webapp.api.chouse_restaurant.router import restaurants_router
from webapp.schema.restaurant.restaurant import RestaurantsListRequest, RestaurantsListResponse


# TODO Доделать
@restaurants_router.post(
    '/list',
    response_model=RestaurantsListResponse,
)
async def rlist(body: RestaurantsListRequest = None):
    pass
