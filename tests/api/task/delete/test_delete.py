from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conf import URLS
from webapp.models.tms.task import Task

BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("task_id", "username", "password", "expected_status", "fixtures"),
    [
        (
            "0",
            "test",
            "test",
            status.HTTP_204_NO_CONTENT,
            [
                FIXTURES_PATH / "tms.user.json",
                FIXTURES_PATH / "tms.category.json",
                FIXTURES_PATH / "tms.task.json",
            ],
        ),
        (
            "0",
            "test1",
            "test1",
            status.HTTP_403_FORBIDDEN,
            [
                FIXTURES_PATH / "tms.user.json",
                FIXTURES_PATH / "tms.category.json",
                FIXTURES_PATH / "tms.task.json",
            ],
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_delete_activity(
    client: AsyncClient,
    task_id: str,
    username: str,
    password: str,
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    task = await db_session.scalars(
        select(Task).where(
            Task.id == task_id,
        )
    )
    assert int(task_id) == task.id

    response = await client.post(
        "".join([URLS["crud"]["task"]["delete"], task_id]),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    task_ids = [
        task.id for task in (await db_session.scalars(select(Task))).all()
    ]
    assert task_id not in task_ids

    assert response.status_code == expected_status
