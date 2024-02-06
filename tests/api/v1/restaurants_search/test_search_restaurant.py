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
            'Beze',
            'Beze',
            'test',
            'qwerty',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.restaurant.json',
            ],
        ),
        (
            'Beze',
            'B',
            'test',
            'qwerty',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.restaurant.json',
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
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_redis_fixture')
async def test_search_restaurant(
    client: AsyncClient,
    expected_name: str | None,
    name: str,
    expected_status: int,
    access_token: str,
    db_session: None,
) -> None:
    request_data = {'name': name}
    response = await client.request(
        'GET', URLS['v1']['restaurants_search'], headers={'Authorization': f'Bearer {access_token}'}, json=request_data
    )
    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        json_response = response.json()
        assert 'restaurants' in json_response

        restaurants = json_response['restaurants']
        assert isinstance(restaurants, list)
        assert len(restaurants) == 1

        restaurant = restaurants[0]
        assert 'name' in restaurant
        assert restaurant['name'] == expected_name
        assert 'location' in restaurant
