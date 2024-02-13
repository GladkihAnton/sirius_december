from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'

@pytest.mark.parametrize(
    ('username', 'password', 'first_name', 'last_name', 'company_name', 'client_id', 'expected_status', 'fixtures'),
    [
        (
            'user',
            'qwerty',
            'Ivan',
            'Russkiy',
            'Sirius',
            2,
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.client.json',
            ],
        )
    ],
)

@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_get_user(
    client: AsyncClient,
    first_name: str,
    last_name: str,
    company_name: str,
    client_id: int,
    expected_status: int,
    access_token: str,
) -> None:
    response = await client.get(
        URLS['client']['get'],
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == expected_status
    response_data = response.json()
    assert first_name == response_data['client']['first_name']
    assert last_name == response_data['client']['last_name']
    assert company_name == response_data['client']['company_name']
    assert client_id == response_data['client']['id']
    