from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import Annotated
from webapp.api.crud.deal.router import deal_router
from webapp.crud.deal import deal_crud
from webapp.integrations.postgres import get_session
from webapp.schema.info.deal import DealInfo
from fastapi.security import OAuth2PasswordRequestForm

from webapp.utils.auth.jwt import oauth2_scheme


@deal_router.post('/create')
async def create_deal(
    body: DealInfo,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    try:
        await deal_crud.create(session, body)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return ORJSONResponse(content={'message': 'Deal created successfully'}, status_code=status.HTTP_201_CREATED)
