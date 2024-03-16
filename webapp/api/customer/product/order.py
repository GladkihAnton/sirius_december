from typing import Any, Dict

from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.customer.product.router import product_router
from webapp.db.postgres import get_session
from webapp.models.sirius.order import Order
from webapp.models.sirius.user_product_feedback import UserProductFeedBack
from webapp.schema.product.feedback import PostFeedBackModel
from webapp.schema.product.order import PostOrderModel
from webapp.utils.auth.jwt import JwtTokenT, validate_customer


@product_router.post('/order')
async def create_order(
    body: PostOrderModel,
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(validate_customer),
) -> ORJSONResponse:
    # TODO INSERT INTO sirius.order ( user_id,product_id,status )
    # 	SELECT user_id, product_id,'pending' as status
    # 	FROM sirius.user_product_feedback
    # 	WHERE user_id = 1 and status = 'liked'
    # ON CONFLICT DO NOTHING

    await session.execute(
        insert(Order).values(
            user_id=access_token['user_id'],
            product_id=body.product_id,
        ).on_conflict_do_nothing()
    )
    await session.commit()


    return ORJSONResponse({'status': 'success'})


def _prepare_response(data: Dict[str, Any]) -> ORJSONResponse:
    return ORJSONResponse(
        {
            'data': data,
        }
    )