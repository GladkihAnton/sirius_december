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
            'John',
            'Doe',
            'Sirius',
            1,
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
        URLS['client']['get'].format(client_id=client_id),
        headers={'Authorization': f'Bearer {access_token}'}
    )
    print(URLS['client']['get'].format(client_id=client_id),)
    assert response.status_code == expected_status
    response_data = response.json()
    print(response_data)
    assert first_name == response_data['cached_client']['first_name']
    assert last_name == response_data['cached_client']['last_name']
    assert company_name == response_data['cached_client']['company_name']
    assert client_id == response_data['cached_client']['id']
