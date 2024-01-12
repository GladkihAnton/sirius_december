from pathlib import Path
from typing import List

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

# Пути к фикстурам
BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('username', 'password', 'expected_status', 'content', 'fixtures'),
    [
        (
            'autotest',
            'qwerty',
            status.HTTP_201_CREATED,
            'This is my new post!',
            [
                FIXTURES_PATH / 'sirius.user.json',
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_kafka_fixture')
async def test_create_post(
    client: AsyncClient,
    username: str,
    password: str,
    access_token: str,
    content: dict,
    expected_status: int,
    kafka_received_messages: List,
):
    headers = {'Authorization': f'Bearer Bearer {access_token}'}
    response = await client.post(
        URLS['posts']['create'],
        json={'content': content},
        headers=headers,
    )
    response_data = response.json()

    assert response.status_code == expected_status
    assert response_data['content'] == content
