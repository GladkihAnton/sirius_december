from webapp.crud.utils.operations import AsyncCRUDFactory
from webapp.models.sirius.tour import Review

review_crud = AsyncCRUDFactory(Review)
