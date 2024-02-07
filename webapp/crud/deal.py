from webapp.crud.utils.operations import AsyncCRUDFactory
from webapp.models.sirius.deal import Deal

deal_crud = AsyncCRUDFactory(Deal)
