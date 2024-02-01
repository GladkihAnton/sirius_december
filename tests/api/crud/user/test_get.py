from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS

from webapp.crud.utils.operations import PAGE_LIMIT
from webapp.models.sirius.user import User
from webapp.schema.info.user import UserInfo

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('page_id', 'username', 'password', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_redis_fixture')
async def test_get(
    client: AsyncClient,
    page_id: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.get(
        ''.join([URLS['crud']['user'], 'page/', page_id]), headers={'Authorization': f'Bearer {access_token}'}
    )

    users = [
        UserInfo.model_validate(tour).model_dump()
        for tour in (await db_session.scalars(select(User).limit(PAGE_LIMIT).offset(int(page_id)))).all()
    ]
    response_reservations = [UserInfo.model_validate(user).model_dump() for user in response.json()['users']]

    assert users == response_reservations

    assert response.status_code == expected_status
