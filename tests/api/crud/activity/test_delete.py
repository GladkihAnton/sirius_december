from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS

from webapp.models.sirius.activity import Activity

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('activity_id', 'username', 'password', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
                FIXTURES_PATH / 'sirius.activity.json',
            ],
        ),
        (
            '0',
            'test1',
            'qwerty',
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
@pytest.mark.usefixtures('_common_api_with_redis_fixture')
async def test_delete_activity(
    client: AsyncClient,
    activity_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    activity_ids = [activity.id for activity in (await db_session.scalars(select(Activity))).all()]
    assert int(activity_id) in activity_ids

    response = await client.delete(
        ''.join([URLS['crud']['activity'], activity_id]),
        headers={'Authorization': f'Bearer {access_token}'},
    )

    activity_ids = [activity.id for activity in (await db_session.scalars(select(Activity))).all()]
    assert activity_id not in activity_ids
    assert response.status_code == expected_status
