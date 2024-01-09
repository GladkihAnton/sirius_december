from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.teacher.router import teacher_router
from webapp.crud.institution import get_institution_by_id
from webapp.crud.teacher import teacher_crud
from webapp.crud.user import get_user_by_id
from webapp.db.postgres import get_session
from webapp.schema.teacher import TeacherInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@teacher_router.put('/update/{teacher_id}')
async def update(
    teacher_id: int,
    body: TeacherInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    # # Check if user exists for creating a relationship
    # if await get_user_by_id(session, body.user_id) is None:
    #     raise HTTPException(detail='User not found', status_code=status.HTTP_404_NOT_FOUND)

    # # Check if institution exists for creating a relationship
    # if await get_institution_by_id(session, body.institution_id) is None:
    #     raise HTTPException(detail='Institution not found', status_code=status.HTTP_404_NOT_FOUND)

    result = await teacher_crud.update(session, body, teacher_id)
    if result is None:
        raise HTTPException(detail='Teacher not found', status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(content={'detail': 'Teacher updated successfully'}, status_code=status.HTTP_200_OK)
