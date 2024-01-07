from webapp.crud.utils.operations import AsyncCRUDFactory
from webapp.models.sirius.reservation import Reservation

reservation_crud = AsyncCRUDFactory(Reservation)
