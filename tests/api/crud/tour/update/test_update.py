from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('tour_id', 'username', 'password', 'expected_status', 'fixtures'),
    [
        (
                '1',
                'test',
                'qwerty',
                status.HTTP_204_NO_CONTENT,
                [
                    FIXTURES_PATH / 'sirius.user.json',
                    FIXTURES_PATH / 'sirius.tour.json',
                ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_get(
        client: AsyncClient,
        tour_id: str,
        expected_status: int,
        access_token: str,
        db_session: None,
) -> None:
    response = await client.post(
        ''.join([URLS['crud']['tour']['update'], tour_id]),
        json={
            "title": "new",
            "price": 10000.0,
            "start_date": "2023-01-28",
            "end_date": "2023-01-28"
        },
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == expected_status
