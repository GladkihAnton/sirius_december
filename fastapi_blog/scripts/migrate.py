import asyncio  # для выполнения асинхронных операций

from webapp.db.postgres import engine  # для подключения к базе данных Postgres
from webapp.models import meta  # для определения метаданных таблиц

# определяется асинхронная функция main, которая создает таблицы в
# базе данных, используя метаданные таблиц из модуля meta


# функция main использует объект engine для
# установления соединения с базой данных
async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(meta.metadata.create_all)


# выполняет операцию создания всех таблиц в базе данных с помощью
# метода create_all() объекта метаданных


if __name__ == '__main__':
    asyncio.run(main())


# если этот скрипт запущен как основной файл (а не импортирован как модуль),
# то вызывается функция main с помощью asyncio.run(),
# чтобы запустить асинхронную функцию в цикле событий asyncio.
# Это создаст все таблицы, необходимые для работы приложения.

# миграция, заполнение