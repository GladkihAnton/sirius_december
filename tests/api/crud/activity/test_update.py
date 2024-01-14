from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS

from webapp.crud.activity import activity_crud
from webapp.crud.utils.operations import PAGE_LIMIT
from webapp.models.sirius.activity import Activity
from webapp.schema.info.activity import ActivityInfo

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('activity_id', 'username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            {'tour_id': 0, 'title': 'zoo', 'place': 'Central zoo', 'type': 'film'},
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.tour.json',
                FIXTURES_PATH / 'sirius.activity.json',
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_update_activity(
    client: AsyncClient,
    activity_id: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    activity_ids = [activity.id for activity in (await db_session.scalars(select(Activity))).all()]
    assert int(activity_id) in activity_ids
    pre_update_data = ActivityInfo.model_validate(
        await activity_crud.get_model(db_session, int(activity_id))
    ).model_dump()

    response = await client.put(
        ''.join([URLS['crud']['activity'], activity_id]),
        json=body,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    activities = [
        ActivityInfo.model_validate(activity).model_dump()
        for activity in (await db_session.scalars(select(Activity).limit(PAGE_LIMIT))).all()
    ]

    assert pre_update_data not in activities
    assert response.status_code == expected_status
