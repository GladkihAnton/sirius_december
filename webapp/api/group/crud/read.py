from typing import List, Optional

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from webapp.api.group.router import group_router
from webapp.cache.cache import redis_get, redis_set
from webapp.crud.const import SKIP_LIMIT
from webapp.crud.group import get_all, get_group_by_id
from webapp.db.postgres import get_session
from webapp.models.sirius.group import Group
from webapp.models.sirius.student import Student
from webapp.schema.group import GroupStudents
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@group_router.get('/page/{page}', response_model=List[GroupStudents])
async def read_all(
    page: int,
    institution_id: Optional[int] = None,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if institution_id is None:
        results = await get_all(session, page)

    else:
        query = (
            select(Group)
            .where(Group.institution_id == institution_id)
            .options(joinedload(Group.students).joinedload(Student.user))
            .limit(SKIP_LIMIT)
            .offset(page)
        )
        results = (await session.execute(query)).unique().scalars().all()

    json_results = [GroupStudents.model_validate(result).model_dump(mode='json') for result in results]

    return ORJSONResponse(json_results)


@group_router.get('/{group_id}', response_model=GroupStudents)
async def read_one(
    group_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    cached = await redis_get(Group.__name__, group_id)
    if cached:
        return ORJSONResponse(cached)

    result = await get_group_by_id(session, group_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    json_result = GroupStudents.model_validate(result).model_dump(mode='json')
    await redis_set(Group.__name__, group_id, json_result)

    return ORJSONResponse(json_result)
