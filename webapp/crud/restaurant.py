from webapp.crud.utils.operations import AsyncCRUDFactory
from webapp.models.sirius.restaurant import Restaurant

restaurant_crud = AsyncCRUDFactory(Restaurant)
