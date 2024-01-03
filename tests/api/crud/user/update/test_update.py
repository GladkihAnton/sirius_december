from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('user_id', 'username', 'new_username', 'password', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'new_user',
            'qwerty',
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
        (
            '0',
            'test1',
            'new_user',
            'qwerty',
            status.HTTP_403_FORBIDDEN,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_update(
    client: AsyncClient,
    user_id: str,
    username: str,
    new_username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: None,
) -> None:
    response = await client.post(
        ''.join([URLS['crud']['user']['update'], user_id]),
        json={'username': new_username, 'password': password},
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == expected_status
