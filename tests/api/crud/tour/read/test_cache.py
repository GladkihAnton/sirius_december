from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('tour_id', 'username', 'password', 'expected_status', 'fixtures'),
    [
        (
            '1',
            'test',
            'qwerty',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_redis_fixture')
async def test_get_users(
    client: AsyncClient,
    tour_id: str,
    expected_status: int,
    access_token: str,
    db_session: None,
) -> None:
    response = await client.get(
        ''.join([URLS['crud']['tour']['read'], tour_id]), headers={'Authorization': f'Bearer {access_token}'}
    )
    assert 'tour' in response.json()
    assert 'cached_tour' not in response.json()
    assert response.status_code == expected_status

    response = await client.get(
        ''.join([URLS['crud']['tour']['read'], tour_id]), headers={'Authorization': f'Bearer {access_token}'}
    )
    assert 'tour' not in response.json()
    assert 'cached_tour' in response.json()
    assert response.status_code == expected_status
