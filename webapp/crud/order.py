from webapp.crud.utils.operations import AsyncCRUDFactory
from webapp.models.sirius.order import Order

order_crud = AsyncCRUDFactory(Order)
