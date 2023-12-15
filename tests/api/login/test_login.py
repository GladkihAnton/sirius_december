import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS


@pytest.mark.parametrize(
    ('username', 'password', 'expected_status'),
    [
        (
            'invalid_user',
            'password',
            status.HTTP_401_UNAUTHORIZED,
        )
    ],
)
@pytest.mark.asyncio()
async def test_login(
    client: AsyncClient,
    username: str,
    password: str,
    expected_status: int,
    db_session: None,
) -> None:
    response = await client.post(URLS['auth']['login'], json={'username': username, 'password': password})

    assert response.status_code == expected_status
