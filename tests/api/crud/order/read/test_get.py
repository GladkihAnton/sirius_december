from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from conf.config import settings
from webapp.models.sirius.order import Order
from webapp.schema.info.order import OrderInfo

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('page_id', 'username', 'password', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            status.HTTP_200_OK,
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
async def test_get_order(
    client: AsyncClient,
    page_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.get(
        ''.join([URLS['crud']['order']['page'], page_id]), headers={'Authorization': f'Bearer {access_token}'}
    )

    orders = [
        OrderInfo.model_validate(order).model_dump()
        for order in (await db_session.scalars(select(Order).limit(settings.PAGE_LIMIT).offset(int(page_id)))).all()
    ]

    assert orders == response.json()['orders']

    assert response.status_code == expected_status
