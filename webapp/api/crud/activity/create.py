from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.activity.router import activity_router
from webapp.crud.activity import activity_crud
from webapp.integrations.postgres import get_session
from webapp.schema.info.activity import ActivityInfo
from webapp.utils.auth.jwt import oauth2_scheme


@activity_router.post('/')
async def create_activity(
    body: ActivityInfo,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    try:
        await activity_crud.create(session, body)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={'message': 'Activity created successfully'}, status_code=status.HTTP_201_CREATED)
