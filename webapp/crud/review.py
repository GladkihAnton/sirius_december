from webapp.crud.utils.operations import AsyncCRUDFactory
from webapp.models.sirius.review import Review

review_crud = AsyncCRUDFactory(Review)
