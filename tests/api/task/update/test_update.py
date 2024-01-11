from pathlib import Path
from typing import Any, Dict

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
    ("task_id", "username", "password", "body", "expected_status", "fixtures"),
    [
        (
            "0",
            "test",
            "test",
            {"tour_id": 0, "title": "zoo", "place": "Central zoo", "type": "film"},
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
async def test_update_activity(
    client: AsyncClient,
    task_id: str,
    body: Dict[str, Any],
    expected_status: int,
    access_token: str,
    db_session: AsyncSession,
) -> None:
    obj: Task = await db_session.scalars(
        select(Task).where(
            Task.id == task_id,
        )
    )
    task = TaskResponse.model_validate(obj).model_dump()
    assert int(task_id) == obj.id

    response = await client.post(
        "".join([URLS["crud"]["task"]["update"], task_id]),
        json=body,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    updated_obj = await db_session.scalars(
        select(Task).where(
            Task.id == task_id,
        )
    )
    updated_task = TaskResponse.model_validate(updated_obj).model_dump()

    assert task != updated_task
    assert response.status_code == expected_status
