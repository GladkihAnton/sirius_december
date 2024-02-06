from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from conf.config import settings
from webapp.crud.order import order_crud
from webapp.models.sirius.order import Order
from webapp.schema.info.order import OrderInfo

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('order_id', 'username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            {'restaurant_id': 0, 'user_id': 0, 'where_to_deliver': '[45.4040001, 39.9540001]'},
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.restaurant.json',
                FIXTURES_PATH / 'sirius.order.json',
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_update_order(
    client: AsyncClient,
    order_id: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    order_ids = [order.id for order in (await db_session.scalars(select(Order))).all()]

    assert int(order_id) in order_ids
    pre_update_data = OrderInfo.model_validate(await order_crud.get_model(db_session, int(order_id))).model_dump()

    response = await client.post(
        ''.join([URLS['crud']['order']['update'], order_id]),
        json=body,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    orders = [
        OrderInfo.model_validate(order).model_dump()
        for order in (await db_session.scalars(select(Order).limit(settings.PAGE_LIMIT))).all()
    ]

    assert pre_update_data not in orders
    assert response.status_code == expected_status
