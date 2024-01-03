from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('user_id', 'username', 'password', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_redis_fixture')
async def test_get(
    client: AsyncClient,
    user_id: str,
    expected_status: int,
    access_token: str,
    db_session: None,
) -> None:
    response = await client.get(
        ''.join([URLS['crud']['user']['read'], user_id]), headers={'Authorization': f'Bearer {access_token}'}
    )
    assert 'user' in response.json()
    assert 'cached_user' not in response.json()
    assert response.status_code == expected_status

    response = await client.get(
        ''.join([URLS['crud']['user']['read'], user_id]), headers={'Authorization': f'Bearer {access_token}'}
    )
    assert 'user' not in response.json()
    assert 'cached_user' in response.json()
    assert response.status_code == expected_status
