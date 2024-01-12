from pathlib import Path
from typing import List

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
        'post_id',
        'content',
        'expected_status',
        'fixtures',
        'kafka_expected_messages',
    ),
    [
        (
            'autotest',
            'qwerty',
            1,
            'Great job!',
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.post.json',
            ],
            [
                {
                    'partition': 1,
                    'topic': 'create_comment',
                    'value': [
                        {
                            'content': 'Great job!',
                        }
                    ],
                }
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_kafka_fixture')
async def test_create_comment(
    client: AsyncClient,
    username: str,
    password: str,
    post_id: int,
    content: str,
    expected_status: int,
    access_token: str,
    kafka_received_messages: List,
    kafka_expected_messages: List,
):
    headers = {'Authorization': f'Bearer Bearer {access_token}'}
    response = await client.post(
        URLS['comments']['create'].format(post_id=post_id),
        json={'content': content},
        headers=headers,
    )

    assert response.status_code == expected_status

    response_data = response.json()

    assert 'id' in response_data
    assert 'content' in response_data
    assert 'author_id' in response_data
    assert response_data['content'] == content
