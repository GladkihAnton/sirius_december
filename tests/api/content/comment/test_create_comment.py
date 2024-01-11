import json
from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.models.meta import metadata

# Пути к фикстурам
USER_FIXTURES_PATH = Path(__file__).parent / 'fixtures' / 'sirius.user.json'
POST_FIXTURES_PATH = Path(__file__).parent / 'fixtures' / 'sirius.post.json'
COMMENT_FIXTURES_PATH = Path(__file__).parent / 'fixtures' / 'sirius.comment.json'


# Загрузка данных комментариев для использования в тестах
with open(COMMENT_FIXTURES_PATH, 'r') as file:
    comment_data = json.load(file)

with open(POST_FIXTURES_PATH, 'r') as file:
    post_data = json.load(file)


@pytest.fixture()
async def _load_fixtures(db_session: AsyncSession):
    # Загрузка данных пользователей
    with open(USER_FIXTURES_PATH, 'r') as user_file:
        user_data = json.load(user_file)
        user_model = metadata.tables['sirius.user']
        await db_session.execute(insert(user_model).values(user_data))
        await db_session.commit()

    # Загрузка данных постов
    with open(POST_FIXTURES_PATH, 'r') as post_file:
        post_data = json.load(post_file)
        post_model = metadata.tables['sirius.post']
        await db_session.execute(insert(post_model).values(post_data))
        await db_session.commit()

    return


# Тест на создание комментария
@pytest.mark.asyncio()
@pytest.mark.usefixtures(
    '_common_api_with_kafka_fixture',
    '_load_fixtures'
)
async def test_create_comment(
    client: AsyncClient,
    access_token: str,
    kafka_received_messages,
):
    headers = {'Authorization': f'Bearer Bearer {access_token}'}
    post_id = int(post_data[0]['id'])
    response = await client.post(
        URLS['comments']['create'].format(post_id=post_id),
        json=comment_data[0],
        headers=headers,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['content'] == comment_data[0]['content']
    assert response.json()['post_id'] == comment_data[0]['post_id']

    assert len(kafka_received_messages) == 1
    kafka_message = kafka_received_messages[0]
    assert kafka_message['topic'] == 'create_comment'
    assert json.loads(kafka_message['value']) == {
        'comment_id': response.json()['id'],
        'content': comment_data[0]['content']
    }