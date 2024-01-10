import asyncio

from webapp.db.postgres import engine
from webapp.models import meta


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(meta.metadata.create_all)

asyncio.run(main())
