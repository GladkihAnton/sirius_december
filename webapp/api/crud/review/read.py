from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.review.router import review_router
from webapp.crud.review import review_crud
from webapp.integrations.cache.cache import redis_get, redis_set
from webapp.integrations.postgres import get_session
from webapp.models.sirius.review import Review
from webapp.schema.info.review import ReviewInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@review_router.get('/page/{page}')
async def get_reviews(
    page: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    serialized_reviews = [
        ReviewInfo.model_validate(review).model_dump() for review in await review_crud.get_page(session, page)
    ]
    return ORJSONResponse({'reviews': serialized_reviews})


@review_router.get('/{review_id}')
async def get_cached_review(
    review_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    if cached := (await redis_get(Review.__name__, review_id)):
        return ORJSONResponse({'cached_review': cached})

    review = await review_crud.get_model(session, review_id)
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_review = ReviewInfo.model_validate(review).model_dump(mode='json')
    await redis_set(Review.__name__, review_id, serialized_review)

    return ORJSONResponse({'review': serialized_review})
