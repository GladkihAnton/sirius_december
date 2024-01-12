from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.models.tms.category import Category
from webapp.schema.category.category import CategoryCreate, CategoryUpdate


async def get_category(session: AsyncSession, category_id: int) -> Category | None:
    return (
        await session.scalars(
            select(Category).where(
                Category.id == category_id,
            )
        )
    ).one_or_none()


async def create_category(
    session: AsyncSession, category_info: CategoryCreate
) -> Category:
    new_category = Category(
        name=category_info.name, description=category_info.description
    )

    session.add(new_category)
    await session.commit()

    return new_category


async def delete_category(session: AsyncSession, category: Category) -> None:
    await session.delete(category)
    await session.commit()


async def update_category(
    session: AsyncSession, category: Category, category_info: CategoryUpdate
) -> Category:
    for key, value in category_info.model_dump().items():
        if value is not None:
            setattr(category, key, value)

    await session.commit()

    return category
