from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from webapp.api.crud.deal.router import deal_router
from webapp.crud.deal import deal_crud
from webapp.integrations.postgres import get_session
from webapp.schema.info.deal import DealInfo
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@deal_router.post('/update/{deal_id}')
async def update_deal(
    body: DealInfo,
    deal_id: int,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    exists = deal_crud.get_model(session, deal_id) is not None

    await deal_crud.update(session, deal_id, body)

    if exists:
        return ORJSONResponse(
            content={'message': 'Deal updated successfully'}, status_code=status.HTTP_204_NO_CONTENT
        )
    return ORJSONResponse(content={'message': 'Deal created successfully'}, status_code=status.HTTP_201_CREATED)
