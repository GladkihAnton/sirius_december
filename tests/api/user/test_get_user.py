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
        'get_username',
        'get_role',
        'full_name',
        'email',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'student1',
            'qwerty',
            11,
            'student1',
            'student',
            'Дмитрий Петров',
            'student1@example.com',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
        (
            'admin1',
            'qwerty',
            11,
            'student1',
            'student',
            'Дмитрий Петров',
            'student1@example.com',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture')
async def test_get_user(
    client: AsyncClient,
    username: str,
    password: str,
    user_id: int,
    get_username: str,
    full_name: str,
    email: str,
    get_role: str,
    expected_status: int,
    access_token: str,
) -> None:
    response = await client.get(
        URLS['user']['get_del_user_by_id'].format(user_id=user_id),
        headers={'Authorization': f'Bearer Bearer {access_token}'},
    )

    assert response.status_code == expected_status
    response_data = response.json()
    assert response_data['role'] == get_role
    assert response_data['additional_info']['full_name'] == full_name
    assert response_data['email'] == email
    assert response_data['username'] == get_username
    assert response_data['id'] == user_id
