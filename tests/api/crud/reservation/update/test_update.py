from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('reservation_id', 'username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            {'user_id': 0, 'tour_id': 0, 'booking_date': '2023-01-29', 'booking_status': 'confirmed'},
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
                FIXTURES_PATH / 'sirius.reservation.json',
            ],
        ),
        (
            '0',
            'test',
            'qwerty',
            {'user_id': 0, 'tour_id': 0, 'booking_date': '2023-29', 'booking_status': 'confirmed'},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
                FIXTURES_PATH / 'sirius.reservation.json',
            ],
        ),
        (
            '0',
            'test0',
            'qwerty',
            {'user_id': 0, 'tour_id': 0, 'booking_date': '2023-01-29', 'booking_status': 'confirmed'},
            status.HTTP_403_FORBIDDEN,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
                FIXTURES_PATH / 'sirius.reservation.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_update(
    client: AsyncClient,
    reservation_id: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: None,
) -> None:
    response = await client.post(
        ''.join([URLS['crud']['reservation']['update'], reservation_id]),
        json=body,
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == expected_status
