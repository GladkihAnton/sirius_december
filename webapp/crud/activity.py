from webapp.crud.utils.operations import AsyncCRUDFactory
from webapp.models.sirius.activity import Activity

activity_crud = AsyncCRUDFactory(Activity)
