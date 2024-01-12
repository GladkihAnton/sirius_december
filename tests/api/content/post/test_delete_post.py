from pathlib import Path
from typing import List

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

# Пути к фикстурам
BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


# Тест на удаление комментария
@pytest.mark.parametrize(
    ('username', 'password', 'post_id', 'expected_status', 'fixtures'),
    [
        (
            'autotest',
            'qwerty',
            1,
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.post.json',
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_kafka_fixture')
async def test_delete_post(
    client: AsyncClient,
    username: str,
    password: str,
    post_id: int,
    expected_status: int,
    access_token: str,
    kafka_received_messages: List,
):
    headers = {'Authorization': f'Bearer Bearer {access_token}'}
    response = await client.delete(
        URLS['posts']['delete'].format(post_id=post_id),
        headers=headers,
    )

    assert response.status_code == expected_status
