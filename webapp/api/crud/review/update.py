from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.review.router import review_router
from webapp.crud.review import review_crud
from webapp.integrations.postgres import get_session
from webapp.schema.info.review import ReviewInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@review_router.post('/update/{review_id}')
async def get_users(
    body: ReviewInfo,
    review_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    try:
        await review_crud.update(session, review_id, body)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(content={'message': 'Review removed successfully'}, status_code=status.HTTP_204_NO_CONTENT)
