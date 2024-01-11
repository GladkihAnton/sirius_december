from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.models.sirius.user import User

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('user_id', 'username', 'password', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_delete_user(
    client: AsyncClient,
    user_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    user_ids = [user.id for user in (await db_session.scalars(select(User))).all()]
    assert int(user_id) in user_ids

    response = await client.post(
        ''.join([URLS['crud']['user']['delete'], user_id]),
        headers={'Authorization': f'Bearer {access_token}'},
    )

    user_ids = [user.id for user in (await db_session.scalars(select(User))).all()]

    assert user_id not in user_ids
    assert response.status_code == expected_status
