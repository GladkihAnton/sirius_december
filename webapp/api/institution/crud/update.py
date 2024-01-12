from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.institution.router import institution_router
from webapp.cache.cache import redis_remove
from webapp.crud.institution import institution_crud
from webapp.db.postgres import get_session
from webapp.models.sirius.institution import Institution
from webapp.schema.institution import InstitutionInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@institution_router.put('/update/{institution_id}')
async def update(
    institution_id: int,
    body: InstitutionInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    result = await institution_crud.update(session, body, institution_id)
    if not result:
        raise HTTPException(detail='Institution not found', status_code=status.HTTP_404_NOT_FOUND)

    await redis_remove(Institution.__name__, institution_id)

    return ORJSONResponse(content={'detail': 'Institution updated successfully'}, status_code=status.HTTP_200_OK)
