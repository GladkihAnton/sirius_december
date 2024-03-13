from typing import Any, Dict

from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.customer.product.router import product_router
from webapp.db.postgres import get_session
from webapp.models.sirius.user_product_feedback import UserProductFeedBack
from webapp.schema.product.feedback import PostFeedBackModel
from webapp.utils.auth.jwt import JwtTokenT, validate_customer


@product_router.post('/feedback')
async def feedback(
    body: PostFeedBackModel,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(validate_customer),
) -> ORJSONResponse:
    await session.execute(
        insert(UserProductFeedBack).values(
            user_id=access_token['user_id'],
            product_id=body.product_id,
            status=body.status,
        )
    )
    await session.commit()


    return ORJSONResponse({'status': 'success'})


def _prepare_response(data: Dict[str, Any]) -> ORJSONResponse:
    return ORJSONResponse(
        {
            'data': data,
        }
    )