from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from webapp.schema.crud import IdField


class Event(BaseModel):
    title: str = Field(description="Название мероприятие", examples=["HighLoad"])
    description: str = Field(description="Описание мероприятие", examples=["IT"])
    date_time: str = Field(description="Дата проведение", examples=["2032-04-23 10:20:30 +02:30"])


class EventDTO(Event):
    @field_validator("date_time")
    @classmethod
    def date_timezone(cls, v: str) -> datetime:
        try:
            dt = datetime.strptime(v, "%Y-%m-%d %H:%M:%S %z")
            return dt
        except ValueError:
            raise ValueError("Неправильный формат времени и часового пояса. %Y-%m-%d %H:%M:%S %z")


class EventResponse(Event, IdField):
    date_time: datetime = Field(description="Дата проведение")
