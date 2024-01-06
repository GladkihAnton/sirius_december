from datetime import date, datetime

from pydantic import BaseModel, field_validator


class TourInfo(BaseModel):
    title: str
    price: float
    start_date: date
    end_date: date

    @field_validator('start_date', 'end_date')
    @classmethod
    def parse_date(cls, value: date | str) -> date:
        if isinstance(value, date):
            return value
        elif isinstance(value, str):
            try:
                return datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Неверный формат даты. Используйте формат YYYY-MM-DD.')
        else:
            raise ValueError('Неверный тип данных. Ожидалась строка или объект date.')
