from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.journal.router import journal_router
from webapp.crud.journal import journal_crud
from webapp.db.postgres import get_session
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@journal_router.delete('/delete/{journal_id}')
async def delete(
    journal_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if not await journal_crud.delete(session, journal_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(content={'detail': 'Journal deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
