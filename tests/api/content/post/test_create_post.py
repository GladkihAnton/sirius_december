import json
from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

BASE_DIR = Path(__file__).parent
POST_FIXTURES_PATH = BASE_DIR / 'fixtures' / 'sirius.post.json'

# Загрузка данных постов для использования в тестах
with open(POST_FIXTURES_PATH, 'r') as file:
    posts_data = json.load(file)


@pytest.mark.parametrize(
    (
        'post',
        'expected_status',
        'expected_content',
        'expected_author_id'
    ),
    [
        (post, status.HTTP_201_CREATED, post['content'], post['author_id'])
        for post in posts_data
    ]
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_kafka_fixture')
async def test_create_post(
    client: AsyncClient,
    access_token: str,
    post: dict,
    expected_status: int,
    expected_content: str,
    expected_author_id: int,
    kafka_received_messages,
):
    headers = {'Authorization': f'Bearer Bearer {access_token}'}

    response = await client.post(
        URLS['posts']['create'],
        json=post,
        headers=headers,
    )

    assert response.status_code == expected_status
    assert response.json()['content'] == expected_content
    assert response.json()['author_id'] == expected_author_id

    assert len(kafka_received_messages) == 1
    kafka_message = kafka_received_messages[0]
    assert kafka_message['topic'] == 'create_post'
    message_value = json.loads(kafka_message['value'])
    assert message_value['content'] == posts_data[0]['content']
    assert message_value['author_id'] == posts_data[0]['author_id']
    assert message_value['post_id'] == response.json()['id']