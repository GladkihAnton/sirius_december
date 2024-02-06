from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.models.sirius.order_product import OrderProduct

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('op_id', 'username', 'password', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            status.HTTP_204_NO_CONTENT,
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
async def test_delete_op(
    client: AsyncClient,
    op_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    op_ids = [op.id for op in (await db_session.scalars(select(OrderProduct))).all()]

    assert int(op_id) in op_ids

    response = await client.post(
        ''.join([URLS['crud']['order_product']['delete'], op_id]),
        headers={'Authorization': f'Bearer {access_token}'},
    )

    op_ids = [op.id for op in (await db_session.scalars(select(OrderProduct))).all()]

    assert op_id not in op_ids
    assert response.status_code == expected_status
