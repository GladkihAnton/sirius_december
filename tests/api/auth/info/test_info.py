from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'password', 'expected_status', 'fixtures'),
    [
        (
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
@pytest.mark.usefixtures('_common_api_fixture')
async def test_login(
    client: AsyncClient,
    username: str,
    password: str,
    access_token: str,
    expected_status: int,
) -> None:
    response = await client.post(URLS['auth']['info'], headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == expected_status
