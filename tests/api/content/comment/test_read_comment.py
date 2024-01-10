import json
from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.const import URLS

from webapp.models.meta import metadata

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

    # Загрузка данных комментариев
    with open(COMMENT_FIXTURES_PATH, 'r') as comment_file:
        comment_data = json.load(comment_file)
        comment_model = metadata.tables['sirius.comment']
        await db_session.execute(insert(comment_model).values(comment_data))
        await db_session.commit()

    return


# Тест на получение комментария
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_fixture', '_load_fixtures')
async def test_read_comment(client: AsyncClient, access_token: str):
    post_id = int(post_data[0]['id'])
    comment_id = int(comment_data[0]['id'])
    comment_content = comment_data[0]['content']
    headers = {'Authorization': f'Bearer Bearer {access_token}'}
    response = await client.get(
        URLS['comments']['read'].format(post_id=post_id),
        headers=headers,
    )
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['comments'][0]['id'] == comment_id
    assert comment_content in response.json()['comments'][0]['content']