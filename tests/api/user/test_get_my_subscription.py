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
        'expected_status',
        'fixtures',
    ),
    [
        (
            'admin1',
            'qwerty',
            status.HTTP_200_OK,
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
async def test_create_user(
    client: AsyncClient,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
) -> None:
    response = await client.get(
        URLS['user']['get_my_subscriptions'],
        headers={'Authorization': f'Bearer Bearer {access_token}'},
    )

    assert response.status_code == expected_status
    response_data = response.json()
    assert len(response_data) == 2
    assert response_data[0]['id'] == 1
    assert response_data[0]['title'] == 'Основы программирования на Python'
    assert response_data[1]['id'] == 2
    assert response_data[1]['title'] == 'Разработка веб-приложений с использованием Django'
