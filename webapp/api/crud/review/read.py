from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.review.router import review_router
from webapp.crud.review import review_crud
from webapp.integrations.cache.cache import redis_get, redis_set
from webapp.integrations.postgres import get_session
from webapp.models.sirius.review import Review
from webapp.schema.info.review import ReviewInfo
from webapp.utils.auth.jwt import oauth2_scheme


@review_router.get('/page/{page}')
async def get_reviews(
    page: int,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    serialized_reviews = [
        ReviewInfo.model_validate(review).model_dump() for review in await review_crud.get_page(session, page)
    ]
    return ORJSONResponse({'reviews': serialized_reviews})


@review_router.get('/{review_id}')
async def get_cached_review(
    review_id: int,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    if cached := (await redis_get(Review.__name__, review_id)):
        return ORJSONResponse({'review': cached})

    review = await review_crud.get_model(session, review_id)
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    serialized_review = ReviewInfo.model_validate(review).model_dump(mode='json')
    await redis_set(Review.__name__, review_id, serialized_review)

    return ORJSONResponse({'review': serialized_review})
