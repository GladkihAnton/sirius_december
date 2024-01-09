from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.institution.router import institution_router
from webapp.crud.institution import institution_crud
from webapp.db.postgres import get_session
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
    if result is None:
        raise HTTPException(detail='Institution not found', status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(content={'detail': 'Institution updated successfully'}, status_code=status.HTTP_200_OK)
