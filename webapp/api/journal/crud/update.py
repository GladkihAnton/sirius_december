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


@journal_router.put('/update/{journal_id}')
async def update(
    journal_id: int,
    body: JournalInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        result = await journal_crud.update(session, body, journal_id)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    if not result:
        raise HTTPException(detail='Journal not found', status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(content={'detail': 'Journal updated successfully'}, status_code=status.HTTP_200_OK)
