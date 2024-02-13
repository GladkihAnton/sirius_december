from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'password', 'title', 'amount', 'date', 'expected_status', 'fixtures'),
    [
        (
            'user',
            'qwerty',
            'Продажа оц',
            1000.123,
            '2024-02-12',
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.deal.json',
                FIXTURES_PATH / 'sirius.user.json',
            ],
        )
    ],
)

@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create_deal(
    client: AsyncClient,
    title: str,
    amount: float,
    date: str,
    expected_status: int,
    access_token: str,
) -> None:
    response = await client.post(
        URLS['deal']['create'],
        json={'title': title, 'amount': amount, 'date': date},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    response_data = response.json()
    assert response.status_code == expected_status