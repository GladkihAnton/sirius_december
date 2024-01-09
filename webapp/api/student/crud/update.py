from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.student.router import student_router
from webapp.crud.group import get_group_by_id
from webapp.crud.institution import get_institution_by_id
from webapp.crud.student import student_crud
from webapp.crud.user import get_user_by_id
from webapp.db.postgres import get_session
from webapp.schema.student import StudentInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@student_router.put('/update/{student_id}')
async def update(
    student_id: int,
    body: StudentInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    # # Check if user exists for creating a relationship
    # if await get_user_by_id(session, body.user_id) is None:
    #     raise HTTPException(detail='User not found', status_code=status.HTTP_404_NOT_FOUND)

    # # Check if institution exists for creating a relationship
    # if await get_institution_by_id(session, body.institution_id) is None:
    #     raise HTTPException(detail='Institution not found', status_code=status.HTTP_404_NOT_FOUND)

    # # Check if group exists for creating a relationship
    # if await get_group_by_id(session, body.group_id) is None:
    #     raise HTTPException(detail='Group not found', status_code=status.HTTP_404_NOT_FOUND)

    result = await student_crud.update(session, body, student_id)
    if result is None:
        raise HTTPException(detail='Student not found', status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(content={'detail': 'Student updated successfully'}, status_code=status.HTTP_200_OK)
