import json
import asyncio  # для выполнения асинхронных операций
from pathlib import Path  # работа с путями файловой системы
from typing import List

from sqlalchemy import insert

from webapp.db.postgres import async_session
from webapp.models.meta import metadata


# определяется асинхронная функция main, которая принимает список имен файлов
# фикстур, загружает данные из каждого файла в соответствующую таблицу
# базы данных и сохраняет изменения.
async def main(fixtures: List[str]) -> None:
    for fixture in fixtures:
        fixture_path = Path(fixture)
        model = metadata.tables[fixture_path.stem]

        with open(fixture_path, 'r') as file:
            values = json.load(file)

        async with async_session() as session:
            await session.execute(insert(model).values(values))
            await session.commit()


# функция main использует модель таблицы из метаданных SQLAlchemy,
# чтобы определить таблицу, в которую будут загружены данные. Затем
# функция открывает JSON-файл, загружает данные и выполняет операцию
# вставки в базу данных с помощью метода execute объекта сессии SQLAlchemy


def process_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('fixtures', nargs='+', help='<Required> Set flag')
    args = parser.parse_args()
    return args.fixtures


if __name__ == '__main__':
    fixtures = process_args()
    asyncio.run(main(fixtures))

# если этот скрипт запущен как основной файл (а не импортирован как модуль),
# то вызывается функция main с аргументами командной строки, переданными в
# качестве списка имен файлов фикстур. Это выполняется с помощью asyncio.run(),
# чтобы запустить асинхронную функцию в цикле событий asyncio
# загрузку данных из JSON-файлов в базу данных с помощью SQLAlchemy и asyncio
