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
    ('username', 'password', 'comment_id', 'expected_status', 'fixtures'),
    [
        (
            'autotest',
            'qwerty',
            1,
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.post.json',
                FIXTURES_PATH / 'sirius.comment.json',
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_kafka_fixture')
async def test_delete_comment(
    client: AsyncClient,
    username: str,
    password: str,
    comment_id: int,
    expected_status: int,
    access_token: str,
    kafka_received_messages: List,
):
    headers = {'Authorization': f'Bearer Bearer {access_token}'}
    response = await client.delete(
        URLS['comments']['delete'].format(comment_id=comment_id),
        headers=headers,
    )

    assert response.status_code == expected_status
