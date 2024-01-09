from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS

from webapp.models.sirius.tour import Tour
from webapp.schema.info.tour import TourInfo

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            'test',
            'qwerty',
            {'title': 'test', 'price': 10000.00, 'start_date': '2023-01-28', 'end_date': '2023-01-28'},
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create_tour(
    client: AsyncClient,
    username: str,
    password: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.post(
        URLS['crud']['tour']['create'], json=body, headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == expected_status
    reviews = [
        TourInfo.model_validate(review).model_dump() for review in (await db_session.scalars(select(Tour))).all()
    ]

    assert TourInfo.model_validate(body).model_dump() in reviews
