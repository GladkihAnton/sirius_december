from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('expected_name', 'name', 'username', 'password', 'expected_status', 'fixtures'),
    [
        (
            'Shaurma Mega',
            'Shaurma Mega',
            'test',
            'qwerty',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.restaurant.json',
                FIXTURES_PATH / 'sirius.product.json',
            ],
        ),
        (
            'Shaurma Mega',
            'Shaurma M',
            'test',
            'qwerty',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.restaurant.json',
                FIXTURES_PATH / 'sirius.product.json',
            ],
        ),
        (
            None,
            'Bveveve',
            'test',
            'qwerty',
            status.HTTP_404_NOT_FOUND,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.restaurant.json',
                FIXTURES_PATH / 'sirius.product.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_redis_fixture')
async def test_search_product(
    client: AsyncClient,
    expected_name: str | None,
    name: str,
    expected_status: int,
    access_token: str,
    db_session: None,
) -> None:
    request_data = {'name': name}
    response = await client.request(
        'GET', URLS['v1']['products_search'], headers={'Authorization': f'Bearer {access_token}'}, json=request_data
    )
    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        json_response = response.json()
        assert 'products' in json_response

        products = json_response['products']
        assert isinstance(products, list)
        assert len(products) == 1

        product = products[0]
        assert 'name' in product
        assert product['name'] == expected_name
        assert 'price' in product
