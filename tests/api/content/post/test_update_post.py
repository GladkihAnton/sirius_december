from pathlib import Path
from typing import List

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

# Пути к фикстурам
BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


# Тест на обновление комментария
@pytest.mark.parametrize(
    (
        'username',
        'password',
        'post_id',
        'updated_content',
        'expected_status',
        'fixtures',
    ),
    [
        (
            'autotest',
            'qwerty',
            1,
            'This is updated post!',
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.post.json',
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture', '_load_fixtures')
async def test_update_post(
    client: AsyncClient,
    access_token: str,
    username: str,
    password: str,
    post_id: int,
    updated_content: str,
    expected_status: int,
    kafka_received_messages: List,
):
    headers = {'Authorization': f'Bearer Bearer {access_token}'}

    response = await client.put(
        URLS['posts']['update'].format(post_id=post_id),
        json={'content': updated_content},
        headers=headers,
    )

    assert response.status_code == expected_status
    assert response.json()['content'] == updated_content
