from webapp.crud.utils.operations import AsyncCRUDFactory
from webapp.models.sirius.client import Client

client_crud = AsyncCRUDFactory(Client)
