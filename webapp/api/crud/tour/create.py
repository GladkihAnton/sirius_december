from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.login.router import auth_router
from webapp.crud.tour import tour_crud
from webapp.integrations.postgres import get_session
from webapp.schema.info.tour import TourInfo


@auth_router.post('/tour/create')
async def create_tour(
    body: TourInfo,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    try:
        await tour_crud.create(session, body)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={'message': 'Tour created successfully'}, status_code=status.HTTP_201_CREATED)
