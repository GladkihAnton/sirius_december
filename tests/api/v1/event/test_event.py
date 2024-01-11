from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

from webapp.models.sirius.event import Event

BASE_DIR = Path(__file__).parent

FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("username", "password", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            [
                FIXTURES_PATH / "sirius.event.json",
                FIXTURES_PATH / "sirius.user.json",
            ],
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_get_event(
    client: AsyncClient,
    username: str,
    password: str,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get(URLS["api"]["v1"]["event"]["event"], headers=headers)
    assert response.status_code == expected_status
    assert len(response.json()) >= 1


@pytest.mark.parametrize(
    (
        "username",
        "password",
        "title",
        "description",
        "date_time",
        "fixtures",
        "expected_status",
    ),
    [
        (
            "test_client",
            "secret",
            "some title",
            "some description",
            "2032-04-23 10:20:30 +02:30",
            [
                FIXTURES_PATH / "sirius.user.json",
            ],
            status.HTTP_201_CREATED,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture_with_redis")
async def test_create_event(
    client: AsyncClient,
    username: str,
    password: str,
    title: str,
    description: str,
    date_time: str,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.post(
        URLS["api"]["v1"]["event"]["event"],
        headers=headers,
        json={"title": title, "description": description, "date_time": date_time},
    )
    assert response.status_code == expected_status
    assert response.json().get("title") == title
    event_id = response.json().get("id")

    new_user_db = await db_session.get(Event, event_id)

    assert new_user_db.title == title


@pytest.mark.parametrize(
    (
        "username",
        "password",
        "title",
        "description",
        "date_time",
        "new_title",
        "fixtures",
        "expected_status",
    ),
    [
        (
            "test_client",
            "secret",
            "some title",
            "some description",
            "2032-04-23 10:20:30 +02:30",
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
async def test_update_event(
    client: AsyncClient,
    username: str,
    password: str,
    title: str,
    description: str,
    date_time: str,
    new_title: str,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.post(
        URLS["api"]["v1"]["event"]["event"],
        headers=headers,
        json={"title": title, "description": description, "date_time": date_time},
    )
    event_id = response.json().get("id")

    response = await client.put(
        URLS["api"]["v1"]["event"]["event"] + "/" + str(event_id),
        headers=headers,
        json={"title": new_title, "description": description, "date_time": date_time},
    )

    assert response.status_code == expected_status
    assert response.json().get("title") == new_title

    event_db = await db_session.get(Event, event_id)

    assert event_db.title == new_title


@pytest.mark.parametrize(
    ("username", "password", "event_id", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            0,
            [
                FIXTURES_PATH / "sirius.user.json",
                FIXTURES_PATH / "sirius.event.json",
            ],
            status.HTTP_204_NO_CONTENT,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture_with_redis")
async def test_delete_event(
    client: AsyncClient,
    username: str,
    password: str,
    event_id: int,
    access_token: str,
    expected_status,
    db_session: None,
) -> None:
    headers = {"Authorization": f"Bearer {  access_token}"}
    old_event = await db_session.get(Event, event_id)
    assert old_event is not None
    response = await client.delete(URLS["api"]["v1"]["event"]["event"] + "/" + str(event_id), headers=headers)
    assert response.status_code == expected_status
    old_event = await db_session.get(Event, event_id)

    assert old_event is None
