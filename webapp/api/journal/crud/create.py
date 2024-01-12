from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.journal.router import journal_router
from webapp.crud.journal import journal_crud
from webapp.db.postgres import get_session
from webapp.schema.journal import JournalInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@journal_router.post('/create')
async def create(
    body: JournalInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        created_id = await journal_crud.create(session, body)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={'id': created_id}, status_code=status.HTTP_201_CREATED)
