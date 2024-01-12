from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.student.router import student_router
from webapp.cache.cache import redis_remove
from webapp.crud.student import student_crud
from webapp.db.postgres import get_session
from webapp.models.sirius.student import Student
from webapp.schema.student import StudentInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@student_router.put('/update/{student_id}')
async def update(
    student_id: int,
    body: StudentInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        result = await student_crud.update(session, body, student_id)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    if not result:
        raise HTTPException(detail='Student not found', status_code=status.HTTP_404_NOT_FOUND)

    await redis_remove(Student.__name__, student_id)

    return ORJSONResponse(content={'detail': 'Student updated successfully'}, status_code=status.HTTP_200_OK)
