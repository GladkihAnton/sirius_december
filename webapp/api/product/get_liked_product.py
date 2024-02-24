from asyncio import QueueEmpty
from typing import Any, Dict, List

import msgpack
from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from webapp.api.product.router import product_router
from webapp.cache.rabbit.key_builder import get_user_products_queue_key
from webapp.db.postgres import get_session
from webapp.db.rabbitmq import get_exchange_users, get_channel
from webapp.models.sirius.product import Product
from webapp.models.sirius.user_product_feedback import UserProductFeedBack
from webapp.schema.product.base import ProductModel
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@product_router.post('/get_liked_product')
async def get_random_product(
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
) -> ORJSONResponse:
    user_product_feedbacks = (await session.scalars(
        select(UserProductFeedBack)
        .where(UserProductFeedBack.user_id == access_token['user_id'])
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