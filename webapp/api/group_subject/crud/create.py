from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.group_subject.router import group_subject_router
from webapp.crud.group_subject import group_subject_crud
from webapp.db.postgres import get_session
from webapp.schema.group_subject import GroupSubjectInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@group_subject_router.post('/create')
async def create(
    body: GroupSubjectInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        created_id = await group_subject_crud.create(session, body)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={'id': created_id}, status_code=status.HTTP_201_CREATED)
