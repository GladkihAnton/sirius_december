from pathlib import Path
from typing import Any, Dict

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from conf.config import settings
from webapp.crud.user import user_crud
from webapp.models.sirius.user import User
from webapp.schema.info.user import UserInfo

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('user_id', 'username', 'password', 'body', 'expected_status', 'fixtures'),
    [
        (
            '0',
            'test',
            'qwerty',
            {'username': 'update_test', 'hashed_password': '123456'},
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_update_user(
    client: AsyncClient,
    user_id: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    user_ids = [user.id for user in (await db_session.scalars(select(User))).all()]

    assert int(user_id) in user_ids
    pre_update_data = UserInfo.model_validate(
        await user_crud.get_model(db_session, int(user_id))
    ).model_dump()

    response = await client.post(
        ''.join([URLS['crud']['user']['update'], user_id]),
        json=body,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    users = [
        UserInfo.model_validate(user).model_dump()
        for user in (await db_session.scalars(select(User).limit(settings.PAGE_LIMIT))).all()
    ]

    assert pre_update_data not in users
    assert response.status_code == expected_status
