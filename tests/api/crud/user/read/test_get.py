from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'password', 'user_id', 'expected_status', 'fixtures'),
    [
        (
            'test',
            'qwerty',
            '1',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
        (
            'test1',
            'qwerty',
            '1',
            status.HTTP_403_FORBIDDEN,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
        (
            'test',
            'qwerty',
            '0',
            status.HTTP_404_NOT_FOUND,
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
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    ('username', 'password', 'user_id', 'expected_status', 'fixtures'),
    [
        (
            'test',
            'qwerty',
            '',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_redis_fixture')
async def test_get_users(
    client: AsyncClient,
    user_id: str,
    expected_status: int,
    access_token: str,
    db_session: None,
) -> None:
    response = await client.get(
        ''.join([URLS['crud']['user']['read'], user_id]), headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == expected_status
