from pathlib import Path
from typing import Any

import pytest
from httpx import AsyncClient
from jose import JWTError, jwt
from starlette import status

from tests.conf import URLS

from conf.config import settings

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'password', 'expected_status', 'expected_access_token', 'fixtures'),
    [
        (
            'invalid_user',
            'password',
            status.HTTP_401_UNAUTHORIZED,
            False,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
        (
            'test',
            'qwerty',
            status.HTTP_200_OK,
            True,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_login(
    client: AsyncClient,
    username: str,
    password: str,
    expected_status: int,
    expected_access_token: Any,
    db_session: None,
) -> None:
    response = await client.post(
        URLS['auth']['token'],
        data={'username': username, 'password': password},
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    )

    assert response.status_code == expected_status

    try:
        jwt.decode(response.json()['access_token'], settings.SECRET_KEY)
        assert expected_access_token
    except (JWTError, KeyError):
        assert not expected_access_token
