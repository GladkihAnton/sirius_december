from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

from webapp.models.sirius.user import User

BASE_DIR = Path(__file__).parent

FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("username", "password", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            [
                FIXTURES_PATH / "sirius.user.json",
            ],
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_get_user(
    client: AsyncClient,
    username: str,
    password: str,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get(URLS["api"]["v1"]["user"]["user"], headers=headers)
    assert response.status_code == expected_status
    assert len(response.json()) >= 1


@pytest.mark.parametrize(
    ("username", "password", "user_id", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            0,
            [
                FIXTURES_PATH / "sirius.user.json",
            ],
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture_with_redis")
async def test_get_user_by_id(
    client: AsyncClient,
    username: str,
    password: str,
    user_id: int,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get(URLS["api"]["v1"]["user"]["user"] + "/" + str(user_id), headers=headers)
    assert response.status_code == expected_status
    assert response.json().get("username") == username


@pytest.mark.parametrize(
    ("username", "password", "new_user", "new_password", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            "test_client2",
            "secret",
            [
                FIXTURES_PATH / "sirius.user.json",
            ],
            status.HTTP_201_CREATED,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture_with_redis")
async def test_create_user(
    client: AsyncClient,
    username: str,
    password: str,
    new_user: str,
    new_password: str,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.post(
        URLS["api"]["v1"]["user"]["user"],
        headers=headers,
        json={"username": new_user, "password": new_password},
    )
    assert response.status_code == expected_status
    assert response.json().get("username") == new_user
    user_id = response.json().get("id")

    new_user_db = await db_session.get(User, user_id)

    assert new_user_db.username == new_user


@pytest.mark.parametrize(
    ("username", "password", "user_id", "new_name", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            0,
            "new_name",
            [
                FIXTURES_PATH / "sirius.user.json",
            ],
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture_with_redis")
async def test_update_user(
    client: AsyncClient,
    username: str,
    password: str,
    user_id: int,
    new_name: str,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get(URLS["api"]["v1"]["user"]["user"] + "/" + str(user_id), headers=headers)
    assert response.json().get("username") == username
    response = await client.put(
        URLS["api"]["v1"]["user"]["user"] + "/" + str(user_id),
        headers=headers,
        json={"username": new_name, "password": password},
    )

    assert response.status_code == expected_status
    assert response.json().get("username") == new_name

    user_db = await db_session.get(User, user_id)

    assert user_db.username == new_name


@pytest.mark.parametrize(
    ("username", "password", "user_id", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            0,
            [
                FIXTURES_PATH / "sirius.user.json",
            ],
            status.HTTP_204_NO_CONTENT,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture_with_redis")
async def test_delete_user(
    client: AsyncClient,
    username: str,
    password: str,
    user_id: int,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {  access_token}"}
    old_user = await db_session.get(User, user_id)
    assert old_user is not None
    response = await client.delete(URLS["api"]["v1"]["user"]["user"] + "/" + str(user_id), headers=headers)
    assert response.status_code == expected_status
    old_user = await db_session.get(User, user_id)

    assert old_user is None
