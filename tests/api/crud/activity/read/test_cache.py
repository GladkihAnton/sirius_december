from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('activity_id', 'username', 'password', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
                FIXTURES_PATH / 'sirius.activity.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_redis_fixture')
async def test_cache_activity(
    client: AsyncClient,
    activity_id: str,
    expected_status: int,
    access_token: str,
    db_session: None,
) -> None:
    response = await client.get(
        ''.join([URLS['crud']['activity']['read'], activity_id]),
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert 'activity' in response.json()
    assert 'cached_activity' not in response.json()
    assert response.status_code == expected_status

    response = await client.get(
        ''.join([URLS['crud']['activity']['read'], activity_id]),
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert 'activity' not in response.json()
    assert 'cached_activity' in response.json()
    assert response.status_code == expected_status

    await client.post(
        ''.join([URLS['crud']['activity']['delete'], activity_id]),
        headers={'Authorization': f'Bearer {access_token}'},
    )

    response = await client.get(
        ''.join([URLS['crud']['activity']['read'], activity_id]),
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
