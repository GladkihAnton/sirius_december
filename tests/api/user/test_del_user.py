from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status
from tests.const import URLS

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    (
        'username',
        'password',
        'user_id',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'student1',
            'qwerty',
            11,
            status.HTTP_403_FORBIDDEN,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
                FIXTURES_PATH / 'sirius.subscription.json',
            ],
        ),
        (
            'admin1',
            'qwerty',
            11,
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.course.json',
                FIXTURES_PATH / 'sirius.subscription.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_delete_user(
    client: AsyncClient,
    username: str,
    password: str,
    user_id: int,
    expected_status: int,
    access_token: str,
) -> None:
    response = await client.delete(
        URLS['user']['get_del_user_by_id'].format(user_id=user_id),
        headers={'Authorization': f'Bearer Bearer {access_token}'},
    )

    assert response.status_code == expected_status
