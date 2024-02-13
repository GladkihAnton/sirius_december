from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'password', 'title', 'amount', 'date', 'deal_id', 'expected_status', 'fixtures'),
    [
        (
            'user',
            'qwerty',
            'Покупка оц',
            1001.12,
            '2024-03-12',
            1,
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.deal.json',
                FIXTURES_PATH / 'sirius.user.json',
            ],
        )
    ],
)

@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_update_deal(
    client: AsyncClient,
    title: str,
    amount: float,
    date: str,
    deal_id: int,
    expected_status: int,
    access_token: str,
) -> None:
    response = await client.post(
        URLS['deal']['update'].format(deal_id=deal_id),
        json={'title': title, 'amount': amount, 'date': date},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    response_data = response.json()
    assert response.status_code == expected_status