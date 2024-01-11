from webapp.crud.utils.operations import AsyncCRUDFactory
from webapp.models.sirius.product import Product

product_crud = AsyncCRUDFactory(Product)
