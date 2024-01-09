from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.group_subject.router import group_subject_router
from webapp.crud.group import get_group_by_id
from webapp.crud.group_subject import group_subject_crud
from webapp.crud.subject import get_subject_by_id
from webapp.db.postgres import get_session
from webapp.schema.group_subject import GroupSubjectInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@group_subject_router.put('/update/{group_subject_id}')
async def update(
    group_subject_id: int,
    body: GroupSubjectInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    # # Check if teacher exists for creating a relationship
    # if await get_teacher_by_id(session, body.teacher_id) is None:
    #     raise HTTPException(detail='Teacher not found', status_code=status.HTTP_404_NOT_FOUND)

    # # Check if institution exists for creating a relationship
    # if await get_institution_by_id(session, body.institution_id) is None:
    #     raise HTTPException(detail='Institution not found', status_code=status.HTTP_404_NOT_FOUND)

    result = await group_subject_crud.update(session, body, group_subject_id)
    if result is None:
        raise HTTPException(
            detail='Relationship between group and subject not found',
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return ORJSONResponse(
        content={'detail': 'Relationship between group and subject updated successfully'},
        status_code=status.HTTP_200_OK,
    )
