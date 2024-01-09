import json
import asyncio
import argparse
from pathlib import Path
from typing import List
from datetime import datetime, time

from sqlalchemy import insert

from webapp.db.postgres import async_session
from webapp.models.meta import metadata

parser = argparse.ArgumentParser()

parser.add_argument('fixtures', nargs='+', help='<Required> Set flag')

args = parser.parse_args()


async def main(fixtures: List[str]) -> None:
    for fixture in fixtures:
        fixture_path = Path(fixture)
        model = metadata.tables[fixture_path.stem]
        with open(fixture_path, 'r') as file:
            values = json.load(file)
            if fixture_path.stem == 'clinic.service':
                for data in values:
                    data['duration'] = time(*map(int, data['duration'].split(':')))
            elif fixture_path.stem == 'clinic.timetable':
                for data in values:
                    data['start'] = datetime.strptime(data['start'], "%Y-%m-%d %H:%M:%S%z")
                    data['end'] = datetime.strptime(data['end'], "%Y-%m-%d %H:%M:%S%z")


        async with async_session() as session:
            await session.execute(insert(model).values(values))
            await session.commit()


if __name__ == '__main__':
    asyncio.run(main(args.fixtures))