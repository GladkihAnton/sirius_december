from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from starlette import status

from tests.conf import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('review_id', 'username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            {'user_id': 0, 'tour_id': 0, 'rating': 4.0, 'comment': 'Good work'},
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
                FIXTURES_PATH / 'sirius.review.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_update(
    client: AsyncClient,
    review_id: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: None,
) -> None:
    response = await client.post(
        ''.join([URLS['crud']['review']['update'], review_id]),
        json=body,
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert response.status_code == expected_status
