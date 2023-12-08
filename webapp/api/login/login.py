import asyncio

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.login.router import auth_router
from webapp.db.postgres import get_session


@auth_router.post('/login')
async def login(session: AsyncSession = Depends(get_session)):
    print(await session.execute(text('select 1')))
    await asyncio.sleep(5)
    print('')
    return {}
