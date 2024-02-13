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
            1000.12,
            '2023-05-30',
            1,
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.deal.json',
                FIXTURES_PATH / 'sirius.user.json',
            ],
        )
    ],
)

@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_get_deals(
    client: AsyncClient,
    title: str,
    amount: float,
    date: str,
    deal_id: str,
    expected_status: int,
    access_token: str,
) -> None:
    response = await client.get(
        URLS['deal']['get'].format(deal_id=deal_id),
        headers={'Authorization': f'Bearer {access_token}'}
    )
    print(response.headers)
    assert response.status_code == expected_status
    response_data = response.json()
    print(response_data)
    assert title == response_data['cached_deal']['title']
    assert amount == response_data['cached_deal']['amount']
    assert date == response_data['cached_deal']['date']
    