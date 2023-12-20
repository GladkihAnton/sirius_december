import asyncio

from sqlalchemy import text

from webapp.db.postgres import async_session, engine
from webapp.models import meta


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(meta.metadata.create_all)

    # TODO костыль #nq
    # async with async_session() as session:
    #     await session.execute(text("ALTER DATABASE main_db OWNER TO postgres;"))
    #     for table in meta.metadata.tables.values():
    #         await session.execute(f"ALTER TABLE {table} OWNER TO postgres;")


if __name__ == '__main__':
    asyncio.run(main())
