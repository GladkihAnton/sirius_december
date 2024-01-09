from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.group_subject.router import group_subject_router
from webapp.crud.group_subject import group_subject_crud
from webapp.db.postgres import get_session
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@group_subject_router.delete('/delete/{group_subject_id}')
async def delete(
    group_subject_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if not await group_subject_crud.delete(session, group_subject_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(
        content={'detail': 'Relationship between group and subject deleted successfully'},
        status_code=status.HTTP_204_NO_CONTENT,
    )
