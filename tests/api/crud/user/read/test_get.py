from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from conf.config import settings
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
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_get_user(
    client: AsyncClient,
    page_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.get(
        ''.join([URLS['crud']['user']['page'], page_id]), headers={'Authorization': f'Bearer {access_token}'}
    )

    users = [
        UserInfo.model_validate(user).model_dump()
        for user in (await db_session.scalars(select(User).limit(settings.PAGE_LIMIT).offset(int(page_id)))).all()
    ]

    assert users == response.json()['users']

    assert response.status_code == expected_status
