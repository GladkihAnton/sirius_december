import json
import asyncio
import argparse
from datetime import datetime
from pathlib import Path
from typing import List

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from webapp.integrations.postgres import async_session
from webapp.models.meta import metadata

parser = argparse.ArgumentParser()

parser.add_argument('fixtures', nargs='+', help='<Required> Set flag')

args = parser.parse_args()


async def main(fixtures: List[str]) -> None:
    for fixture in fixtures:
        fixture_path = Path(fixture)
        model_name = fixture_path.stem
        model = metadata.tables[model_name]

        with open(fixture_path, 'r') as file:
            values = json.load(file)

        for model_obj in values:
            for key, val in model_obj.items():
                if 'date' in key:
                    model_obj[key] = datetime.strptime(val, '%Y-%m-%d').date()

        async with async_session() as session:
            for model_obj in values:
                username = model_obj.get('username')
                if username:
                    stmt = select(model).where(model.c.username == username)
                    result = await session.execute(stmt)
                    existing_record = result.scalar()
                    if existing_record:
                        print(f"Skipping insert for {username}. Entry already exists.")
                        continue

                try:
                    await session.execute(insert(model).values(model_obj))
                    await session.commit()
                    print(f"Inserted data for {username}.")
                except IntegrityError as e:
                    print(f'IntegrityError: Unique constraint violation - {str(e)}')


if __name__ == '__main__':
    asyncio.run(main(args.fixtures))
