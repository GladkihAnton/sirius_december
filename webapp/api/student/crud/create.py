from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.student.router import student_router
from webapp.crud.student import student_crud
from webapp.db.postgres import get_session
from webapp.schema.student import StudentInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@student_router.post('/create')
async def create(
    body: StudentInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        created_id = await student_crud.create(session, body)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={'id': created_id}, status_code=status.HTTP_201_CREATED)
