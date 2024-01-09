from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.tms.category import Category
from webapp.schema.category.category import CategoryCreate


async def get_category(session: AsyncSession, task_id: int) -> Category | None:
    return (
        await session.scalars(
            select(Category).where(
                Category.id == task_id,
            )
        )
    ).one_or_none()

async def create_category(session: AsyncSession, category_info: CategoryCreate) -> None:
    new_category = Category(
        name=category_info.name,
        description=category_info.description
    )

    session.add(new_category)
    await session.commit()