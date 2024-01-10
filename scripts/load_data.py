import json
import asyncio
import argparse
from datetime import datetime
from pathlib import Path
from typing import List

from sqlalchemy import insert

from webapp.integrations.postgres import async_session
from webapp.models.meta import metadata

parser = argparse.ArgumentParser()

parser.add_argument('fixtures', nargs='+', help='<Required> Set flag')

args = parser.parse_args()


async def main(fixtures: List[str]) -> None:
    for fixture in fixtures:
        fixture_path = Path(fixture)
        model_name = fixture_path.stem

        if model_name not in metadata.tables:
            print(f"Table '{model_name}' not found in metadata.")
            continue

        model = metadata.tables[model_name]

        with open(fixture_path, 'r') as file:
            values = json.load(file)

        for model_obj in values:
            for key, val in model_obj.items():
                if 'date' in key:
                    model_obj[key] = datetime.strptime(val, '%Y-%m-%d').date()

        async with async_session() as session:
            await session.execute(insert(model).values(values))
            await session.commit()

if __name__ == '__main__':
    asyncio.run(main(args.fixtures))
