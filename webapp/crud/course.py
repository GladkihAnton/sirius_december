from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from webapp.models.sirius.course import Course
from webapp.models.sirius.subscribe import Subscription
from webapp.schema.education.course import CourseCreate, CourseRead


async def create_course(session: AsyncSession, course_data: CourseCreate) -> CourseRead:
    new_course = Course(**course_data.model_dump())
    session.add(new_course)
    await session.commit()
    await session.refresh(new_course)
    return CourseRead.model_validate(new_course)


async def get_courses_all(session: AsyncSession, page: int, page_size: int) -> List[CourseRead] | None:
    result = await session.execute(select(Course).offset((page - 1) * page_size).limit(page_size))
    all_courses = result.scalars().all()
    if all_courses:
        return [CourseRead.model_validate(course) for course in all_courses]
    return None


async def get_course_by_id(session: AsyncSession, course_id: int) -> CourseRead | None:
    result = await session.execute(
        select(Course).where(Course.id == course_id).options(joinedload(Course.subscriptions))
    )
    course = result.scalars().first()
    if course:
        return CourseRead.model_validate(course)
    return None


async def update_course(session: AsyncSession, course_id: int, course_data: CourseCreate) -> CourseRead | None:
    result = await session.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if course:
        for var, value in vars(course_data).items():
            setattr(course, var, value) if value else None
        await session.commit()
        await session.refresh(course)
        return CourseRead.model_validate(course)
    return None


async def get_courses_subscription(session: AsyncSession, user_id: int) -> List[CourseRead] | None:
    course_ids_subquery = select(Subscription.course_id).where(Subscription.user_id == user_id).subquery()
    courses = await session.execute(
        select(Course).where(Course.id.in_(course_ids_subquery)).options(selectinload(Course.lessons))
    )
    courses = courses.scalars().all()
    return [CourseRead.model_validate(course) for course in courses]


async def delete_course(session: AsyncSession, course_id: int) -> bool:
    result = await session.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if course:
        await session.delete(course)
        await session.commit()
        return True
    return False
