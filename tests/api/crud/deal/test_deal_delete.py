from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'password', 'deal_id', 'expected_status', 'fixtures'),
    [
        (
            'user',
            'qwerty',
            1,
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.deal.json',
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_delete_deal(
    client: AsyncClient,
    deal_id: int,
    expected_status: int,
    access_token: str,
) -> None:
    response = await client.post(
        URLS['deal']['delete'].format(deal_id=deal_id),
        headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == expected_status
