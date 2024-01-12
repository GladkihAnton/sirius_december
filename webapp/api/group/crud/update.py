from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.group.router import group_router
from webapp.cache.cache import redis_remove
from webapp.crud.group import group_crud
from webapp.db.postgres import get_session
from webapp.models.sirius.group import Group
from webapp.schema.group import GroupInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@group_router.put('/update/{group_id}')
async def update(
    group_id: int,
    body: GroupInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        result = await group_crud.update(session, body, group_id)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    if not result:
        raise HTTPException(detail='Group not found', status_code=status.HTTP_404_NOT_FOUND)

    await redis_remove(Group.__name__, group_id)

    return ORJSONResponse(content={'detail': 'Group updated successfully'}, status_code=status.HTTP_200_OK)
