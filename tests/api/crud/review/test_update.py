from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS

from webapp.crud.review import review_crud
from webapp.crud.utils.operations import PAGE_LIMIT
from webapp.models.sirius.review import Review
from webapp.schema.info.review import ReviewInfo

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
async def test_update_review(
    client: AsyncClient,
    review_id: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    review_ids = [review.id for review in (await db_session.scalars(select(Review))).all()]
    assert int(review_id) in review_ids
    pre_update_data = ReviewInfo.model_validate(await review_crud.get_model(db_session, int(review_id))).model_dump()

    response = await client.put(
        ''.join([URLS['crud']['review'], review_id]),
        json=body,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    reviews = [
        ReviewInfo.model_validate(review).model_dump()
        for review in (await db_session.scalars(select(Review).limit(PAGE_LIMIT))).all()
    ]

    assert pre_update_data not in reviews
    assert response.status_code == expected_status
