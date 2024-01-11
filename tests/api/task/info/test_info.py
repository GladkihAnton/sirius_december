from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS
from webapp.models.tms.task import Task
from webapp.schema.task.task import TaskResponse

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("task_id", "username", "password", "expected_status", "fixtures"),
    [
        (
            "0",
            "test",
            "test",
            status.HTTP_200_OK,
            [
                FIXTURES_PATH / "tms.user.json",
                FIXTURES_PATH / "tms.category.json",
                FIXTURES_PATH / "tms.task.json",
            ],
        )
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_get_activity(
    client: AsyncClient,
    task_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    response = await client.get(
        "".join([URLS["crud"]["task"]["read"], task_id]),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    obj = await db_session.scalars(
        select(Task).where(
            Task.id == task_id,
        )
    )
    task = TaskResponse.model_validate(obj).model_dump()

    assert task == response.json()["result"]

    assert response.status_code == expected_status
