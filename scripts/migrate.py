import asyncio

from webapp.db.postgres import engine
from webapp.models.meta import metadata


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


if __name__ == '__main__':
    asyncio.run(main())
