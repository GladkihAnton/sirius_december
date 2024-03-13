from typing import Any, Dict, List

from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from webapp.api.customer.product.router import product_router
from webapp.db.postgres import get_session
from webapp.models.sirius.user_product_feedback import UserProductFeedBack, StatusFeedbackEnum
from webapp.schema.product.base import ProductModel
from webapp.utils.auth.jwt import JwtTokenT, validate_customer


@product_router.post('/get_liked_product')
async def get_liked_product(
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(validate_customer),
) -> ORJSONResponse:
    user_product_feedbacks = (await session.scalars(
        select(UserProductFeedBack)
        .where(
            UserProductFeedBack.user_id == access_token['user_id'],
            UserProductFeedBack.status == StatusFeedbackEnum.liked,
        )
        .options(joinedload(UserProductFeedBack.product))
    )).all()
    serialized_products = [
        ProductModel.model_validate(user_product_feedbacks.product).model_dump(mode='json')
        for user_product_feedbacks in user_product_feedbacks
    ]


    return _prepare_response(serialized_products)


def _prepare_response(data: List[Dict[str, Any]]) -> ORJSONResponse:
    return ORJSONResponse(
        {
            'data': data,
        }
    )