from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.router import crud_router
from webapp.crud.tour import tour_crud
from webapp.crud.user import user_crud
from webapp.integrations.postgres import get_session
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@crud_router.get('/tour/delete')
async def delete_tour(
    tour_id: int | None = None,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    user = await user_crud.get(session, tour_id)  # type: ignore
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await tour_crud.delete(session, tour_id)

    return ORJSONResponse(content={'message': 'Tour removed successfully'}, status_code=status.HTTP_204_NO_CONTENT)
