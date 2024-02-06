from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from conf.config import settings
from webapp.crud.product import product_crud
from webapp.models.sirius.product import Product
from webapp.schema.info.product import ProductInfo

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('product_id', 'username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            {'restaurant_id': 0, 'name': 'Shaurma Small', 'price': 199.99},
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.restaurant.json',
                FIXTURES_PATH / 'sirius.product.json',
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_update_product(
    client: AsyncClient,
    product_id: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    product_ids = [product.id for product in (await db_session.scalars(select(Product))).all()]

    assert int(product_id) in product_ids
    pre_update_data = ProductInfo.model_validate(await product_crud.get_model(db_session, int(product_id))).model_dump()

    response = await client.post(
        ''.join([URLS['crud']['product']['update'], product_id]),
        json=body,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    products = [
        ProductInfo.model_validate(product).model_dump()
        for product in (await db_session.scalars(select(Product).limit(settings.PAGE_LIMIT))).all()
    ]

    assert pre_update_data not in products
    assert response.status_code == expected_status
