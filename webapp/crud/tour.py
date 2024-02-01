from webapp.crud.utils.operations import AsyncCRUDFactory
from webapp.models.sirius.tour import Tour

tour_crud = AsyncCRUDFactory(Tour)
