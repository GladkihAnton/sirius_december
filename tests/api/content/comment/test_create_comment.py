import json
from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

# Пути к фикстурам
BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'

with open(FIXTURES_PATH / 'sirius.user.json', 'r') as file:
    user_data = json.load(file)
# Загрузка данных для использования в тестах
with open(FIXTURES_PATH / 'sirius.comment.json', 'r') as file:
    comment_data = json.load(file)


# Тест на создание комментария
@pytest.mark.parametrize(
    (
        'expected_status',
        'expected_status_token',
        'fixtures'
    ),
    [
        (
            status.HTTP_201_CREATED,
            True,
            [
                FIXTURES_PATH / 'sirius.user.json'
            ]
        )
    ]
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_kafka_fixture')
async def test_create_comment(
    client: AsyncClient,
    access_token: str,
    kafka_received_messages,
    post_id: int,
    comment_data: dict,
    fixtures: list,
):
    headers = {'Authorization': f'Bearer Bearer {access_token}'}
    response = await client.post(
        URLS['comments']['create'].format(post_id=post_id),
        json=comment_data[0]['content'],
        headers=headers,
    )

    # Проверки ответа и сообщений Kafka
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['content'] == comment_payload['content']
    assert response.json()['post_id'] == post_id

    assert len(kafka_received_messages) == 1
    kafka_message = kafka_received_messages[0]
    assert kafka_message['topic'] == 'create_comments'
    assert json.loads(kafka_message['value']) == {
        'comment_id': response.json()['id'],
        'content': comment_payload['content']
    }