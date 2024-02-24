from asyncio import QueueEmpty
from typing import Any, Dict

import msgpack
from fastapi import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.api.product.router import product_router
from webapp.cache.rabbit.key_builder import get_user_products_queue_key
from webapp.db.postgres import get_session
from webapp.db.rabbitmq import get_exchange_users, get_channel
from webapp.models.sirius.product import Product
from webapp.models.sirius.user_product_feedback import UserProductFeedBack
from webapp.schema.product.base import ProductModel
from webapp.schema.product.feedback import PostFeedBackModel
from webapp.utils.auth.jwt import JwtTokenT, jwt_auth


@product_router.post('/feedback')
async def feedback(
    body: PostFeedBackModel = Depends(),
    session: AsyncSession = Depends(get_session),
    access_token: JwtTokenT = Depends(jwt_auth.validate_token),
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