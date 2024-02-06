from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from webapp.models.sirius.subscribe import Subscription


async def create_subscription(session: AsyncSession, user_id: int, course_id: int) -> bool:
    new_subscription = Subscription(user_id=user_id, course_id=course_id)
    if new_subscription:
        session.add(new_subscription)
        await session.commit()
        await session.refresh(new_subscription)
        return True
    return False


async def delete_subscription(session: AsyncSession, user_id: int, course_id: int) -> bool:
    result = await session.execute(
        select(Subscription).where(Subscription.user_id == user_id, Subscription.course_id == course_id)
    )
    subscription = result.scalars().first()
    if subscription:
        await session.delete(subscription)
        await session.commit()
        return True
    return False
