import asyncio
import logging

from sqlalchemy.exc import IntegrityError

from webapp.db.postgres import engine
from webapp.models import meta


async def main() -> None:
    try:
        async with engine.begin() as conn:
            await conn.run_sync(meta.metadata.create_all)
    except IntegrityError:
        logging.exception('Already exists')


if __name__ == '__main__':
    asyncio.run(main())
