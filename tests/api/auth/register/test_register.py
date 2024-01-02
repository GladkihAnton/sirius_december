from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'password', 'expected_status', 'fixtures'),
    [
        (
            'invalid_user',
            'qwerty',
            status.HTTP_409_CONFLICT,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
        (
            'test',
            'qwerty',
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_login(
    client: AsyncClient,
    username: str,
    password: str,
    expected_status: int,
    db_session: None,
) -> None:
    response = await client.post(URLS['auth']['register'], json={'username': username, 'password': password})

    assert response.status_code == expected_status
