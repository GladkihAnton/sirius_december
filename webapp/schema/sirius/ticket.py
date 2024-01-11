from pydantic import BaseModel, Field
from pydantic_async_validation import async_field_validator

from webapp.crud.event import get_event_by_id
from webapp.crud.user import get_user_by_id
from webapp.db.postgres import get_session
from webapp.schema.crud import IdField


class Ticket(BaseModel):
    user_id: int = Field(description="ID Пользователя", examples=[1])
    event_id: int = Field(description="ID Мероприятия", examples=[1])


class TicketDTO(Ticket):
    @async_field_validator("user_id")
    async def exist_user(self, value: int) -> int:
        async with get_session() as session:
            user = await get_user_by_id(await session, value)
        if not user:
            raise ValueError(f"Пользователь с id = {value} не найден")
        return value

    @async_field_validator("event_id")
    async def exist_event(self, value: int) -> int:
        async with get_session() as session:
            user = await get_event_by_id(await session, value)
        if not user:
            raise ValueError(f"Мероприятие с id = {value} не найден")
        return value


class TicketResponse(Ticket, IdField):
    pass
