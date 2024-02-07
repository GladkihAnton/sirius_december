from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('name', 'user_id', 'expected_status', 'fixtures'),
    [
        (
            'John Doe',
            1,
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create_employee(
    client: AsyncClient,
    name: str,
    user_id: int,
    expected_status: int,
) -> None:
    response = await client.post(
        URLS['employee']['create'],
        json={'name': name, 'user_id': user_id},
    )

    assert response.status_code == expected_status
    response_data = response.json()
    assert response_data['name'] == name
    assert response_data['user_id'] == user_id
