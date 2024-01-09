from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.institution.router import institution_router
from webapp.crud.institution import institution_crud
from webapp.db.postgres import get_session
from webapp.schema.institution import InstitutionInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@institution_router.post('/create')
async def create(
    body: InstitutionInfo,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        created_id = await institution_crud.create(session, body)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={'id': created_id}, status_code=status.HTTP_201_CREATED)
