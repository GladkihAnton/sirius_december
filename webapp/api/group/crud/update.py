from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.group.router import group_router
from webapp.crud.group import group_crud
from webapp.crud.institution import get_institution_by_id
from webapp.db.postgres import get_session
from webapp.schema.group import GroupInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@group_router.put('/update/{group_id}')
async def update(
    group_id: int,
    body: GroupInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    # # Check if institution exists for creating a relationship
    # if await get_institution_by_id(session, body.institution_id) is None:
    #     raise HTTPException(detail='Institution not found', status_code=status.HTTP_404_NOT_FOUND)

    result = await group_crud.update(session, body, group_id)
    if result is None:
        raise HTTPException(detail='Group not found', status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(content={'detail': 'Group updated successfully'}, status_code=status.HTTP_200_OK)
