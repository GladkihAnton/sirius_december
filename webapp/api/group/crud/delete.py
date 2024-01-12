from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.group.router import group_router
from webapp.cache.cache import redis_remove
from webapp.crud.group import group_crud
from webapp.db.postgres import get_session
from webapp.models.sirius.group import Group
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@group_router.delete('/delete/{group_id}')
async def delete(
    group_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if not await group_crud.delete(session, group_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await redis_remove(Group.__name__, group_id)

    return ORJSONResponse(content={'detail': 'Group deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT)
