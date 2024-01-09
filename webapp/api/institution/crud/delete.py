from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.institution.router import institution_router
from webapp.crud.institution import institution_crud
from webapp.db.postgres import get_session
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@institution_router.delete('/delete/{institution_id}')
async def delete(
    institution_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if not await institution_crud.delete(session, institution_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(
        content={'detail': 'Institution deleted successfully'}, status_code=status.HTTP_204_NO_CONTENT
    )
