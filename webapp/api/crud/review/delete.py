from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.router import crud_router
from webapp.crud.review import review_crud
from webapp.integrations.postgres import get_session
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@crud_router.get('/review/delete')
async def delete_review(
    tour_id: int | None = None,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    review = await review_crud.get(session, tour_id)  # type: ignore
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await review_crud.delete(session, tour_id)

    return ORJSONResponse(content={'message': 'Review removed successfully'}, status_code=status.HTTP_204_NO_CONTENT)
