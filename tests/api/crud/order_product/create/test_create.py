from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.models.sirius.order_product import OrderProduct
from webapp.schema.info.order_product import OPInfo

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            'test',
            'qwerty',
            {'order_id': 0, 'product_id': 0, 'quantity': 25},
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.restaurant.json',
                FIXTURES_PATH / 'sirius.product.json',
                FIXTURES_PATH / 'sirius.order.json',
                FIXTURES_PATH / 'sirius.order_product.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create_op(
    client: AsyncClient,
    username: str,
    password: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.post(
        URLS['crud']['order_product']['create'], json=body, headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == expected_status

    ops = [OPInfo.model_validate(op).model_dump() for op in (await db_session.scalars(select(OrderProduct))).all()]

    assert body in ops
