from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'password', 'first_name', 'last_name', 'company_name', 'expected_status', 'fixtures'),
    [
        (
            'user',
            'qwerty',
            'Oleg',
            'Mongol',
            'Baltika',
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.client.json',
                FIXTURES_PATH / 'sirius.user.json',
            ],
        )
    ],
)

@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create_client(
    client: AsyncClient,
    first_name: str,
    last_name: str,
    company_name: str,
    expected_status: int,
    access_token: str,
) -> None:
    response = await client.post(
        URLS['client']['create'],
        json={'first_name': first_name, 'last_name': last_name, 'company_name': company_name},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    response_data = response.json()
    assert response.status_code == expected_status