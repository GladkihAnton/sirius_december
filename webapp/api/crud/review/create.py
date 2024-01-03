from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.review.router import review_router
from webapp.crud.review import review_crud
from webapp.integrations.postgres import get_session
from webapp.schema.auth.review import ReviewInfo


@review_router.post('/create')
async def create_review(
    body: ReviewInfo,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    try:
        await review_crud.create(session, body)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={'message': 'Review created successfully'}, status_code=status.HTTP_201_CREATED)
