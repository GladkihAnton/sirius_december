from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.subject.router import subject_router
from webapp.cache.cache import redis_remove
from webapp.crud.subject import subject_crud
from webapp.db.postgres import get_session
from webapp.models.sirius.subject import Subject
from webapp.schema.subject import SubjectInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@subject_router.put('/update/{subject_id}')
async def update(
    subject_id: int,
    body: SubjectInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        result = await subject_crud.update(session, body, subject_id)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    if not result:
        raise HTTPException(detail='Subject not found', status_code=status.HTTP_404_NOT_FOUND)

    await redis_remove(Subject.__name__, subject_id)

    return ORJSONResponse(content={'detail': 'Subject updated successfully'}, status_code=status.HTTP_200_OK)
