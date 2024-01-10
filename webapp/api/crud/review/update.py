from fastapi import Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.review.router import review_router
from webapp.crud.review import review_crud
from webapp.integrations.cache.cache import redis_drop_key
from webapp.integrations.postgres import get_session
from webapp.models.sirius.review import Review
from webapp.schema.info.review import ReviewInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@review_router.post('/update/{review_id}')
async def update_review(
    body: ReviewInfo,
    review_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> Response:
    exists = review_crud.get_model(session, review_id) is not None

    await review_crud.update(session, review_id, body)

    await redis_drop_key(Review.__name__, review_id)

    if exists:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return Response(content={'message': 'Review created successfully'}, status_code=status.HTTP_201_CREATED)
