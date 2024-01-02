from typing import List

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.review.utils.get_review import get_review_model
from webapp.api.crud.router import crud_router
from webapp.crud.review import review_crud
from webapp.integrations.postgres import get_session
from webapp.models.sirius.user import User
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth
from webapp.utils.crud.serializers import serialize_model


@crud_router.get('/review')
async def get_review(
    review_id: int | None = None,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if review_id is None:
        reviews: List[User] = list(await review_crud.get_all(session))
        serialized_reviews = serialize_model(reviews)
        return ORJSONResponse({'reviews': serialized_reviews})

    review = await get_review_model(session, review_id)
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_review = serialize_model(review)
    return ORJSONResponse({'review': serialized_review})
