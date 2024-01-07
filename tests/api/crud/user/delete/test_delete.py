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
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
        (
            '0',
            'test1',
            'qwerty',
            status.HTTP_403_FORBIDDEN,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
        (
            '-1',
            'test',
            'qwerty',
            status.HTTP_404_NOT_FOUND,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_delete(
    client: AsyncClient,
    user_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: None,
) -> None:
    response = await client.post(
        ''.join([URLS['crud']['user']['delete'], user_id]), headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == expected_status
