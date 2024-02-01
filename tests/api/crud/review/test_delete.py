from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS

from webapp.models.sirius.review import Review

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('review_id', 'username', 'password', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
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
async def test_delete_review(
    client: AsyncClient,
    review_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    review_ids = [review.id for review in (await db_session.scalars(select(Review))).all()]
    assert int(review_id) in review_ids

    response = await client.delete(
        ''.join([URLS['crud']['review'], review_id]), headers={'Authorization': f'Bearer {access_token}'}
    )

    review_ids = [review.id for review in (await db_session.scalars(select(Review))).all()]
    assert review_id not in review_ids
    assert response.status_code == expected_status
