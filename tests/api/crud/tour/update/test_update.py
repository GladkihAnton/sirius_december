from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('tour_id', 'username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            {'title': 'new', 'price': 10000.0, 'start_date': '2023-01-28', 'end_date': '2023-01-28'},
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
            ],
        ),
        (
            '0',
            'test',
            'qwerty',
            {'title': 'new', 'price': 10000.0, 'start_date': '2023-01-28', 'end_date': '2023-28'},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
            ],
        ),
        (
            '0',
            'tes',
            'qwerty',
            {'title': 'new', 'price': 10000.0, 'start_date': '2023-01-28', 'end_date': '2023-28'},
            status.HTTP_403_FORBIDDEN,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_update(
    client: AsyncClient,
    tour_id: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: None,
) -> None:
    response = await client.post(
        ''.join([URLS['crud']['tour']['update'], tour_id]),
        json=body,
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == expected_status
