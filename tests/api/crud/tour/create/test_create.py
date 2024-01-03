from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            'invalid_user',
            'qwerty',
            {
                "title": "test",
                "price": 10000.00,
                "start_date": "28/01/23  08:20:00",
                "end_date": "28/01/23  08:20:00"
            },
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
        (
            'test',
            'qwerty',
            {
                "title": "test",
                "price": 10000.00,
                "start_date": "28/01/23  08:20:00",
                "end_date": "28/01/23  08:20:00"
            },
            status.HTTP_409_CONFLICT,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_register(
    client: AsyncClient,
    username: str,
    password: str,
    body: dict,
    expected_status: int,
    db_session: None,
) -> None:
    response = await client.post(URLS['auth']['register'], json={'username': username, 'password': password})

    assert response.status_code == expected_status
