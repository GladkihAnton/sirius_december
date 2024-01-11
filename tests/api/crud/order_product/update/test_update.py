from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from conf.config import settings
from webapp.crud.order_product import op_crud
from webapp.models.sirius.order_product import OrderProduct
from webapp.schema.info.order_product import OPInfo

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('op_id', 'username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            {'order_id': 0, 'product_id': 0, 'quantity': 5},
            status.HTTP_204_NO_CONTENT,
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
async def test_update_order(
    client: AsyncClient,
    op_id: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    op_ids = [op.id for op in (await db_session.scalars(select(OrderProduct))).all()]

    assert int(op_id) in op_ids
    pre_update_data = OPInfo.model_validate(await op_crud.get_model(db_session, int(op_id))).model_dump()

    response = await client.post(
        ''.join([URLS['crud']['order_product']['update'], op_id]),
        json=body,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    ops = [
        OPInfo.model_validate(op).model_dump()
        for op in (await db_session.scalars(select(OrderProduct).limit(settings.PAGE_LIMIT))).all()
    ]

    assert pre_update_data not in ops
    assert response.status_code == expected_status
