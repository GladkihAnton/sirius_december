from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.deal.router import deal_router
from webapp.crud.deal import deal_crud
from webapp.integrations.postgres import get_session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from webapp.utils.auth.jwt import oauth2_scheme


@deal_router.post('/delete/{deal_id}')
async def delete_deal(
    deal_id: int,
    access_token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session), #C помощью класса Depends() в функцию передается результат функции get_session, то есть сессия базы данных, который передается параметру session.
) -> ORJSONResponse:
    if not await deal_crud.delete(session, deal_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return ORJSONResponse(
        content={'message': 'Deal removed successfully'}, status_code=status.HTTP_204_NO_CONTENT
    )
