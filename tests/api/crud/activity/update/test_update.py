from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('activity_id', 'username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            '1',
            'test',
            'qwerty',
            {'tour_id': 1, 'title': 'zoo', 'place': 'Central zoo', 'type': 'film'},
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
                FIXTURES_PATH / 'sirius.activity.json',
            ],
        ),
        (
            '1',
            'test1',
            'qwerty',
            {'tour_id': 1, 'title': 'zoo', 'place': 'Central zoo', 'type': 'film'},
            status.HTTP_403_FORBIDDEN,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
                FIXTURES_PATH / 'sirius.activity.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_update(
    client: AsyncClient,
    activity_id: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: None,
) -> None:
    response = await client.post(
        ''.join([URLS['crud']['activity']['update'], activity_id]),
        json=body,
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == expected_status
