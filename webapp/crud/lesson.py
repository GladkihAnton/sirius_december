from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from webapp.models.sirius.lesson import Lesson
from webapp.schema.education.lesson import LessonCreate, LessonRead


async def create_lesson(session: AsyncSession, course_id: int, lesson_data: LessonCreate) -> LessonRead:
    new_lesson = Lesson(course_id=course_id, **lesson_data.model_dump())
    session.add(new_lesson)
    await session.commit()
    await session.refresh(new_lesson)
    return LessonRead.model_validate(new_lesson)


async def get_lessons_all_by_course_id(
    session: AsyncSession,
    course_id: int,
    page: int = 1,
    page_size: int = 10,
) -> Optional[List[LessonRead]]:
    # рассчет смещения на основе номера страницы и размера страницы
    offset = (page - 1) * page_size
    # выполняем запрос с учетом смещения и лимита
    result = await session.execute(select(Lesson).where(Lesson.course_id == course_id).offset(offset).limit(page_size))
    all_lessons = result.scalars().all()
    if all_lessons:
        return [LessonRead.model_validate(lesson) for lesson in all_lessons]
    return None


async def get_lesson_by_id(session: AsyncSession, course_id: int, lesson_id: int) -> LessonRead | None:
    result = await session.execute(select(Lesson).where(Lesson.id == lesson_id, Lesson.course_id == course_id))
    lesson = result.scalars().first()
    if lesson:
        return LessonRead.model_validate(lesson)
    return None


async def update_lesson(
    session: AsyncSession, course_id: int, lesson_id: int, lesson_data: LessonCreate
) -> LessonRead | None:
    result = await session.execute(select(Lesson).where(Lesson.id == lesson_id, Lesson.course_id == course_id))
    lesson = result.scalars().first()
    if lesson:
        for var, value in lesson_data.dict(exclude_unset=True).items():
            setattr(lesson, var, value)
        await session.commit()
        await session.refresh(lesson)

        # преобразование данных из объекта SQLAlchemy в словарь
        lesson_dict = {
            'id': lesson.id,
            'course_id': lesson.course_id,
            'title': lesson.title,
            'content': lesson.content,
            'order': lesson.order,
            'uploaded_at': lesson.uploaded_at,
        }

        # создание экземпляра модели Pydantic из словаря
        lesson_read = LessonRead(**lesson_dict)
        return lesson_read
    return None


async def delete_lesson(session: AsyncSession, course_id: int, lesson_id: int) -> bool:
    result = await session.execute(select(Lesson).where(Lesson.id == lesson_id, Lesson.course_id == course_id))
    lesson = result.scalars().first()
    if lesson:
        await session.delete(lesson)
        await session.commit()
        return True
    return False
