from typing import List

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.institution.router import institution_router
from webapp.cache.cache import redis_get, redis_set
from webapp.crud.institution import get_all, get_institution_by_id
from webapp.db.postgres import get_session
from webapp.models.sirius.institution import Institution
from webapp.schema.institution import InstitutionRead
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@institution_router.get('/page/{page}', response_model=List[InstitutionRead])
async def read_all(
    page: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    results = await get_all(session, page)
    json_results = [InstitutionRead.model_validate(result).model_dump(mode='json') for result in results]

    return ORJSONResponse(json_results)


@institution_router.get('/{institution_id}', response_model=InstitutionRead)
async def read_one(
    institution_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    cached = await redis_get(Institution.__name__, institution_id)
    if cached:
        return ORJSONResponse(cached)

    result = await get_institution_by_id(session, institution_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    json_result = InstitutionRead.model_validate(result).model_dump(mode='json')
    await redis_set(Institution.__name__, institution_id, json_result)

    return ORJSONResponse(json_result)
