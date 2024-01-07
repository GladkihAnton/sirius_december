from pathlib import Path
from typing import Any

import pytest
from httpx import AsyncClient
from jose import JWTError, jwt
from starlette import status

from tests.const import URLS

from conf.config import settings

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


@pytest.mark.parametrize(
    ('post_content', 'expected_status', 'expected_in_response', 'fixtures'),
    [
        ('New post content', status.HTTP_201_CREATED, True, [FIXTURES_PATH / 'sirius.user.json']),
        ('', status.HTTP_400_BAD_REQUEST, False, [FIXTURES_PATH / 'sirius.user.json']),
    ],
)
@pytest.mark.asyncio
@pytest.mark.usefixtures('_common_api_fixture')
async def test_create_post(
    client: AsyncClient,
    access_token: str,
    post_content: str,
    expected_status: int,
    expected_in_response: bool,
    db_session: None,
):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = await client.post(URLS['posts']['create'], json={'content': post_content}, headers=headers)
    print(response.text)
    assert response.status_code == expected_status
    if expected_in_response:
        assert 'id' in response.json()
    else:
        assert 'id' not in response.json()


@pytest.mark.asyncio
@pytest.mark.usefixtures('_common_api_fixture')
async def test_read_post(
    client: AsyncClient,
    access_token: str,
    db_session: None,
):
    # Получение post_id, например, из предыдущего теста или фикстуры
    post_id = '1'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = await client.get(URLS['posts']['read'].format(post_id=post_id), headers=headers)

    assert response.status_code == status.HTTP_200_OK
    # Дополнительные проверки содержимого ответа


@pytest.mark.asyncio
@pytest.mark.usefixtures('_common_api_fixture')
async def test_update_post(
    client: AsyncClient,
    access_token: str,
    db_session: None,
):
    post_id = '1'
    updated_content = 'Updated content'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = await client.put(URLS['posts']['update'].format(post_id=post_id), json={'content': updated_content}, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    # Проверить, что контент был обновлен

@pytest.mark.asyncio
@pytest.mark.usefixtures('_common_api_fixture')
async def test_delete_post(
    client: AsyncClient,
    access_token: str,
    db_session: None,
):
    post_id = '1'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = await client.delete(URLS['posts']['delete'].format(post_id=post_id), headers=headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Проверить, что пост был удален