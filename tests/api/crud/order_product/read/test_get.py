from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from conf.config import settings
from webapp.models.sirius.order_product import OrderProduct
from webapp.schema.info.order_product import OPInfo

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
                FIXTURES_PATH / 'sirius.product.json',
                FIXTURES_PATH / 'sirius.order.json',
                FIXTURES_PATH / 'sirius.order_product.json',
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_get_op(
    client: AsyncClient,
    page_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.get(
        ''.join([URLS['crud']['order_product']['page'], page_id]), headers={'Authorization': f'Bearer {access_token}'}
    )

    ops = [
        OPInfo.model_validate(op).model_dump()
        for op in (await db_session.scalars(select(OrderProduct).limit(settings.PAGE_LIMIT).offset(int(page_id)))).all()
    ]

    assert ops == response.json()['ops']

    assert response.status_code == expected_status
