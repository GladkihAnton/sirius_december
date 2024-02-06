from webapp.crud.utils.operations import AsyncCRUDFactory
from webapp.models.sirius.order_product import OrderProduct

op_crud = AsyncCRUDFactory(OrderProduct)
