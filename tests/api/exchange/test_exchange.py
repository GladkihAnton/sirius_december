from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

from webapp.models.sirius.exchange import Exchange

BASE_DIR = Path(__file__).parent

FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("username", "password", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            [
                FIXTURES_PATH / "sirius.exchange.json",
                FIXTURES_PATH / "sirius.user.json",
            ],
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_get_exchange(
    client: AsyncClient,
    username: str,
    password: str,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get(URLS["api"]["exchange"]["exchange"], headers=headers)
    assert response.status_code == expected_status
    assert len(response.json()) >= 1


@pytest.mark.parametrize(
    (
        "username",
        "password",
        "title",
        "fixtures",
        "expected_status",
    ),
    [
        (
            "test user",
            "secret",
            "some title",
            [
                FIXTURES_PATH / "sirius.user.json",
            ],
            status.HTTP_201_CREATED,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture_with_redis")
async def test_create_exchange(
    client: AsyncClient,
    username: str,
    password: str,
    title: str,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.post(
        URLS["api"]["exchange"]["exchange"],
        headers=headers,
        json={"title": title},
    )
    assert response.status_code == expected_status
    assert response.json().get("title") == title
    exchange_id = response.json().get("id")

    new_user_db = await db_session.get(Exchange, exchange_id)

    assert new_user_db.title == title


@pytest.mark.parametrize(
    (
        "username",
        "password",
        "title",
        "new_title",
        "fixtures",
        "expected_status",
    ),
    [
        (
            "test_client",
            "secret",
            "some title",
            "new_title",
            [
                FIXTURES_PATH / "sirius.user.json",
            ],
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture_with_redis")
async def test_update_exchange(
    client: AsyncClient,
    username: str,
    password: str,
    title: str,
    new_title: str,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.post(
        URLS["api"]["exchange"]["exchange"],
        headers=headers,
        json={"title": title},
    )
    exchange_id = response.json().get("id")

    response = await client.put(
        URLS["api"]["exchange"]["exchange"] + "/" + str(exchange_id),
        headers=headers,
        json={"title": new_title},
    )

    assert response.status_code == expected_status
    assert response.json().get("title") == new_title

    exchange_db = await db_session.get(Exchange, exchange_id)

    assert exchange_db.title == new_title


@pytest.mark.parametrize(
    ("username", "password", "exchange_id", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            0,
            [
                FIXTURES_PATH / "sirius.user.json",
                FIXTURES_PATH / "sirius.exchange.json",
            ],
            status.HTTP_204_NO_CONTENT,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture_with_redis")
async def test_delete_exchange(
    client: AsyncClient,
    username: str,
    password: str,
    exchange_id: int,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {  access_token}"}
    old_exchange = await db_session.get(Exchange, exchange_id)
    assert old_exchange is not None
    response = await client.delete(URLS["api"]["exchange"]["exchange"] + "/" + str(exchange_id), headers=headers)
    assert response.status_code == expected_status
    old_exchange = await db_session.get(Exchange, exchange_id)

    assert old_exchange is None
