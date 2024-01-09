from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.journal.router import journal_router
from webapp.crud.journal import journal_crud
from webapp.crud.student import get_student_by_id
from webapp.crud.subject import get_subject_by_id
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
    # # Check if student exists for creating a relationship
    # if await get_student_by_id(session, body.student_id) is None:
    #     raise HTTPException(detail='Student not found', status_code=status.HTTP_404_NOT_FOUND)

    # # Check if subject exists for creating a relationship
    # if await get_subject_by_id(session, body.subject_id) is None:
    #     raise HTTPException(detail='Subject not found', status_code=status.HTTP_404_NOT_FOUND)

    result = await journal_crud.update(session, body, journal_id)
    if result is None:
        raise HTTPException(detail='Journal not found', status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(content={'detail': 'Journal updated successfully'}, status_code=status.HTTP_200_OK)
