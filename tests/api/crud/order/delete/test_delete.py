from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.models.sirius.order import Order

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('order_id', 'username', 'password', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.restaurant.json',
                FIXTURES_PATH / 'sirius.order.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_delete_order(
    client: AsyncClient,
    order_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    order_ids = [order.id for order in (await db_session.scalars(select(Order))).all()]

    assert int(order_id) in order_ids

    response = await client.post(
        ''.join([URLS['crud']['order']['delete'], order_id]),
        headers={'Authorization': f'Bearer {access_token}'},
    )

    order_ids = [order.id for order in (await db_session.scalars(select(Order))).all()]

    assert order_id not in order_ids
    assert response.status_code == expected_status
