from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            'test',
            'qwerty',
            {'tour_id': 0, 'title': 'zoo', 'place': 'Central zoo', 'type': 'excursion'},
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create(
    client: AsyncClient,
    username: str,
    password: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: None,
) -> None:
    response = await client.post(
        URLS['crud']['activity']['create'], json=body, headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == expected_status
